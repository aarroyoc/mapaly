import re
import uuid

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from quiz.models import Quiz, Question, Map
from editor.upload import upload_image, delete_image


def slugizer(name):
    name = name.lower()
    name = re.sub(r"\s", r"-", name)
    code = str(uuid.uuid4())[0:6]
    name = f"{name}-{code}"
    return name


class NewView(LoginRequiredMixin, View):
    def get(self, request):
        english_maps = Map.objects.filter(language="en")
        spanish_maps = Map.objects.filter(language="es")
        context = {"english": english_maps, "spanish": spanish_maps}
        return render(request, "editor/new.html", context)

    def post(self, request):
        quiz = Quiz()
        quiz.author = request.user
        quiz.name = request.POST["name"]
        quiz.map = Map.objects.get(pk=int(request.POST["map"]))
        quiz.slug = slugizer(request.POST["name"])
        quiz.save()
        return redirect("editor", quiz.slug)


class EditorView(LoginRequiredMixin, View):
    def get(self, request, slug):
        quiz = Quiz.objects.get(slug=slug)
        questions = Question.objects.filter(quiz=quiz)
        context = {
            "quiz": quiz,
            "questions": questions,
        }
        return render(request, "editor/editor.html", context)

    def post(self, request, slug):
        quiz = Quiz.objects.get(slug=slug)
        question = Question()
        question.question = request.POST["question"]
        question.answer = request.POST["answer"]
        question.quiz = quiz
        question.save()
        return self.get(request, slug)


class DashboardView(LoginRequiredMixin, ListView):
    paginate_by = 20
    template_name = "editor/dashboard.html"

    def get_queryset(self):
        return Quiz.objects.filter(author=self.request.user).order_by("-created_at")


class DeleteMapView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        context = {"quiz": quiz}
        return render(request, "editor/delete.html", context)

    def post(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        if quiz.author == request.user:
            quiz.delete()
        return redirect("dashboard")


@login_required
def delete_question(request, pk):
    question = Question.objects.get(pk=pk)
    if question.quiz.author == request.user:
        question.delete()
        return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    else:
        return HttpResponse(status=403)


@login_required
def publish_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if quiz.author != request.user:
        return HttpResponse(status=403)

    if quiz.front_image is None or not quiz.description:
        return HttpResponse(status=412)

    quiz.status = Quiz.QuizStatus.PUBLISHED
    quiz.save()
    return redirect("quiz", quiz.slug)


@login_required
def remix_quiz(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    remix = Quiz()
    remix.author = request.user
    remix.description = quiz.description
    remix.map = quiz.map
    remix.name = f"{quiz.name} Remix"
    remix.slug = slugizer(remix.name)
    remix.save()

    questions = Question.objects.filter(quiz=quiz)
    for question in questions:
        remix_question = Question()
        remix_question.quiz = remix
        remix_question.question = question.question
        remix_question.answer = question.answer
        remix_question.save()

    return redirect("editor", remix.slug)


@login_required
def save_quiz_settings(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    if quiz.author != request.user:
        return HttpResponse(status_code=403)
    if description := request.POST.get("description"):
        quiz.description = description
    if request.FILES.get("front_image"):
        image_to_delete = None
        if quiz.front_image is not None:
            image_to_delete = quiz.front_image
        quiz.front_image = upload_image(request.FILES["front_image"])
        if image_to_delete is not None:
            delete_image(image_to_delete)
    quiz.save()
    return redirect("editor", quiz.slug)
