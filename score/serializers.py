from rest_framework import serializers
from django.contrib.auth.models import User

from quiz.models import Quiz
from score.models import Score

class ScoreSerializer(serializers.ModelSerializer):
    quiz = serializers.SlugRelatedField(slug_field='slug', queryset=Quiz.objects.all())
    user = serializers.SlugRelatedField(slug_field='username', queryset=User.objects.all())

    def validate_user(self, value):
        if value.username != self.context["request"].user.username:
            raise serializers.ValidationError("Invalid username")
        return value

    class Meta:
        model = Score
        fields = ["quiz", "user", "score", "time"]