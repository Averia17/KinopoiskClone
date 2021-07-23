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
        return Film.objects.filter(type='FILM')




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
