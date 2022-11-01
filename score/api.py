from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import AllowAny

from score.models import Score
from score.serializers import ScoreSerializer


class ScoreAPI(ListCreateAPIView):
    serializer_class = ScoreSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs["slug"]
        return Score.objects.filter(quiz__slug=slug).order_by("-score", "time")[0:10]


@api_view(["GET"])
def me(request):
    return Response({"username": request.user.username})
