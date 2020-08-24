from django import forms

from quiz.models import Quiz

class QuizForm(forms.ModelForm):
    class Meta:
        model = Quiz
        exclude = ("created_at", "modified_at", "author", "slug")
        widgets = {
            'description': forms.Textarea(attrs={'cols': 20, 'rows': 3}),
        }