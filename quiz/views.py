from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views.generic import View, ListView
from quiz.models import Quiz


class QuizView(View):
    def get(self, request, slug):
        try:
            quiz = Quiz.objects.get(slug=slug)
            context = {
                "slug": quiz.slug
            }
            return render(request, "quiz/quiz.html", context)
        except Quiz.DoesNotExist:
            return HttpResponseNotFound()


class HomeView(ListView):
    paginate_by = 20
    template_name = "quiz/home.html"

    def get_queryset(self):
        return Quiz.objects.filter(status=Quiz.QuizStatus.PUBLISHED).order_by("-created_at")
