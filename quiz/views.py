import random
from django.http.response import Http404

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound, HttpResponseBadRequest
from django.views.generic import View, ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from lunr import lunr

from quiz.models import Quiz, QuizComment


class QuizView(View):
    def get(self, request, slug):
        try:
            quiz = Quiz.objects.get(slug=slug)
            comments = QuizComment.objects.filter(author=quiz.author).order_by(
                "created_at"
            )
            context = {
                "quiz": quiz,
                "comments": comments,
                "num_comments": len(comments),
            }
            return render(request, "quiz/quiz.html", context)
        except Quiz.DoesNotExist:
            return HttpResponseNotFound()


def get_local_queryset(request):
    qs = Quiz.objects.filter(status=Quiz.QuizStatus.PUBLISHED).order_by("-created_at")
    if request.COOKIES.get("show_all_lang"):
        return qs
    else:
        language_code = request.LANGUAGE_CODE[0:2]
        if language_code not in ["en", "es"]:
            language_code = "en"
        return qs.filter(map__language=language_code)


class HomeView(ListView):
    paginate_by = 20
    template_name = "quiz/home.html"

    def get_queryset(self):
        return get_local_queryset(self.request)

    def get_context_data(self, **kwargs):
        language_code = self.request.LANGUAGE_CODE
        context = super().get_context_data(**kwargs)
        context["top"] = Quiz.objects.filter(
            status=Quiz.QuizStatus.PUBLISHED, map__language=language_code, top=True
        ).order_by("-created_at")[0:5]
        context["language"] = self.request.COOKIES.get("show_all_lang", language_code)
        return context


class ProfileView(ListView):
    paginate_by = 20
    template_name = "quiz/profile.html"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs["user"])
        return Quiz.objects.filter(
            status=Quiz.QuizStatus.PUBLISHED, author=user
        ).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["username"] = self.kwargs["user"]
        return context


class SearchView(ListView):
    paginate_by = 20
    template_name = "quiz/search.html"

    def get_queryset(self):
        """
        query = self.request.GET["q"]
        q1 = Quiz.objects.filter(name__icontains=query)
        q2 = Quiz.objects.filter(description__icontains=query)
        return q1.union(q2)
        """
        # Lunr could be replaced by ElasticSearch in if gets slow
        # First call to Lunr is long: downloads NLTK data
        query = self.request.GET.get("q")
        if query is None or query == "":
            raise Http404("")

        docs = Quiz.objects.filter(status=Quiz.QuizStatus.PUBLISHED).values(
            "id", "name", "description"
        )
        idx = lunr(
            ref="id",
            fields=("name", "description"),
            documents=docs,
            languages=["en", "es"],
        )
        result = [result["ref"] for result in idx.search(query)]
        return Quiz.objects.filter(id__in=result)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET["q"]
        return context


@login_required
def add_comment(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk)
    comment = QuizComment.objects.create(
        quiz=quiz, author=request.user, content=request.POST["content"]
    )
    comment.save()
    return redirect("quiz", quiz.slug)


def set_language(request):
    response = redirect("home")
    lang = request.GET.get("lang", None)
    if lang == "all":
        response.set_cookie("show_all_lang", "all")
    else:
        response.delete_cookie("show_all_lang")
        response.set_cookie("django_language", lang)
    return response


def get_random_quiz(request):
    pks = get_local_queryset(request).values_list("pk", flat=True)
    random_pk = random.choice(pks)
    random_quiz = Quiz.objects.get(pk=random_pk)
    return redirect("quiz", random_quiz.slug)
