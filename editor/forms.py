from django import forms

from quiz.models import Quiz


class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        fields = ("name", "description", "map")
        labels = {
            "name": "Nombre",
            "description": "Descripción",
            "map": "Mapa"
        }
        widgets = {
            'description': forms.Textarea(attrs={'cols': 20, 'rows': 3}),
        }
