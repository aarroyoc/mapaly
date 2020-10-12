from django import forms
from django.utils.translation import gettext_lazy as _

from quiz.models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("name", "map", "language")
        labels = {
            "name": _("Name"),
            "map": _("Base map"),
            "language": _("Language"),
        }
