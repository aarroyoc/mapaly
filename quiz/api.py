from rest_framework.generics import RetrieveAPIView
from quiz.models import Quiz
from quiz.serializers import QuizSerializer


class QuizDetailAPI(RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    lookup_field = "slug"
