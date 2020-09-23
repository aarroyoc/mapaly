from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.views.generic import View, ListView
from django.contrib.auth.models import User

from quiz.models import Quiz


class QuizView(View):
    def get(self, request, slug):
        try:
            quiz = Quiz.objects.get(slug=slug)
            context = {
                "quiz": quiz
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