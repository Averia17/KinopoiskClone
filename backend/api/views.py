from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import FilmSerializer
from .services import get_top_films
from ..models import Film


class MainPageView(APIView):

    def get(self, request, *args, **kwargs):
        films = get_top_films()

        serializer = FilmSerializer(films, many=True)
        return Response(serializer.data)