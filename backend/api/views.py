from rest_framework import viewsets

from .serializers import FilmListSerializer, StaffSerializer, FilmSerializer, StaffListSerializer
from ..models import Film, Staff
from .services import check_if_empty_films


class FilmsViewSet(viewsets.ModelViewSet):

    serializer_class = FilmSerializer

    action_to_serializer = {
        "list": FilmListSerializer,
        "retrieve": FilmSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )

    @staticmethod
    def get_queryset():
        #check_if_empty_films()
        # Полная дичь но слайсы нельзя делать...
        # n = 0
        # films = []
        # for film in Film.objects.filter(type='FILM').order_by('-rating'):
        #     if n == 250:
        #         return films
        #     films.append(film)
        #
        #     n += 1
        return Film.objects.filter(type='FILM').order_by('-rating')


class SerialsViewSet(viewsets.ModelViewSet):

    serializer_class = FilmSerializer

    action_to_serializer = {
        "list": FilmListSerializer,
        "retrieve": FilmSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )

    @staticmethod
    def get_queryset():
        #check_if_empty_films()
        # Полная дичь но слайсы нельзя делать...
        # n = 0
        # films = []
        # for film in Film.objects.filter(type='TV_SHOW').order_by('-rating'):
        #     if n == 250:
        #         return films
        #     films.append(film)
        #
        #     n += 1
        #Film.objects.filter(type='TV_SHOW').order_by('-rating')
        return Film.objects.filter(type='TV_SHOW').order_by('-rating')


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer

    @staticmethod
    def get_queryset():
        return Staff.objects.all()

    action_to_serializer = {
        "list": StaffListSerializer,
        "retrieve": StaffSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


