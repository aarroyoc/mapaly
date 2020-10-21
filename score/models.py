from django.db import models
from django.contrib.auth.models import User

from quiz.models import Quiz

class Score(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    time = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)