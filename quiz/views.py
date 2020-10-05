from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseNotFound
from django.views.generic import View, ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from lunr import lunr

from quiz.models import Quiz, QuizComment


class QuizView(View):
    def get(self, request, slug):
        try:
            quiz = Quiz.objects.get(slug=slug)
            comments = QuizComment.objects.filter(author=quiz.author).order_by("created_at")
            context = {
                "quiz": quiz,
                "comments": comments,
                "num_comments": len(comments),
            }
            return render(request, "quiz/quiz.html", context)
        except Quiz.DoesNotExist:
            return HttpResponseNotFound()


class HomeView(ListView):
    paginate_by = 20
    template_name = "quiz/home.html"

    def get_queryset(self):
        return Quiz.objects.filter(status=Quiz.QuizStatus.PUBLISHED).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["top"] = Quiz.objects.filter(status=Quiz.QuizStatus.PUBLISHED, top=True).order_by("-created_at")[0:5]
        return context


class ProfileView(ListView):
    paginate_by = 20
    template_name = "quiz/profile.html"

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs["user"])
        return Quiz.objects.filter(status=Quiz.QuizStatus.PUBLISHED, author=user).order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user"] = self.kwargs["user"]
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
        query = self.request.GET["q"]
        docs = Quiz.objects.filter(status=Quiz.QuizStatus.PUBLISHED).values("id", "name", "description")
        idx = lunr(ref="id", fields=("name", "description"), documents=docs, languages=["en", "es"])
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
        quiz=quiz,
        author=request.user,
        content=request.POST["content"]
    )
    comment.save()
    return redirect("quiz", quiz.slug)