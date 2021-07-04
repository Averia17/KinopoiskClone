from rest_framework import viewsets

from .serializers import FilmSerializer
from ..models import Film


class FilmsViewSet(viewsets.ModelViewSet):
    queryset = Film.objects.all()
    serializer_class = FilmSerializer
