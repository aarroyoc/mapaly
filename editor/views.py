from django.shortcuts import render, redirect
from django.views.generic import View, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from quiz.models import Quiz

class DashboardView(LoginRequiredMixin, ListView):
    paginate_by = 20
    template_name = "editor/dashboard.html"

    def get_queryset(self):
        return Quiz.objects.filter(author=self.request.user).order_by("-created_at")


class DeleteMapView(LoginRequiredMixin, View):
    def get(self, request, pk):
        quiz = Quiz.objects.get(pk=pk)
        context = {
            "quiz": quiz
        }
        return render(request, "editor/delete.html", context)

    def post(self, request, pk):
        try:
            quiz = Quiz.objects.get(pk=pk)
            if quiz.author == request.user:
                quiz.delete()
        except:
            pass
        return redirect("dashboard")
