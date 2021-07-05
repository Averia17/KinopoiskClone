from rest_framework import viewsets

from .serializers import FilmSerializer
from ..models import Film
from .services import check_if_empty_films


class FilmsViewSet(viewsets.ModelViewSet):

    serializer_class = FilmSerializer

    def get_queryset(self):
        check_if_empty_films()
        return Film.objects.all()
