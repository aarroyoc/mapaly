from django.db import models
from django.contrib.auth.models import User

from mapaly.settings import AZURE_STORAGE_CONTAINER_FRONT_PREFIX

class Map(models.Model):
    name = models.CharField(max_length=150)
    content = models.TextField()
    license = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    class QuizStatus(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    slug = models.SlugField(max_length=150, unique=True, allow_unicode=True)
    name = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    map = models.ForeignKey(Map, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=2, choices=QuizStatus.choices, default=QuizStatus.DRAFT)
    front_image = models.TextField(blank=False)
    top = models.BooleanField(default=False)

    @property
    def front_image_url(self):
        return f"{AZURE_STORAGE_CONTAINER_FRONT_PREFIX}{self.front_image}"


class QuizComment(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name="questions")
    question = models.CharField(max_length=200)
    answer = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
