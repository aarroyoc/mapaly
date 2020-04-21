from django.shortcuts import render
from django.http import HttpResponseNotFound
from django.views.generic import View
from quiz.models import Quiz, Question

import json


class QuizView(View):
    def get(self, request, slug):
        try:
            quiz = Quiz.objects.get(slug=slug)
            quiz_data = {
                "questions": list(Question.objects.values("question", "answer").filter(quiz=quiz)),
            }
            context = {
                "quiz": quiz,
                "quiz_data": json.dumps(quiz_data),
            }
            return render(request, "quiz/quiz.html", context)
        except Quiz.DoesNotExist:
            return HttpResponseNotFound()
