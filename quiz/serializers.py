from rest_framework import serializers

from quiz.models import Quiz, Map, Question


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = ["name", "content", "license"]


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["question", "answer"]


class QuizSerializer(serializers.ModelSerializer):
    map = MapSerializer()
    questions = QuestionSerializer(many=True)

    class Meta:
        model = Quiz
        fields = ["map", "slug", "name", "description", "questions"]
