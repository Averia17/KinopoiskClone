from rest_framework import viewsets

from .serializers import FilmSerializer, StaffSerializer
from ..models import Film, Staff
from .services import check_if_empty_films


class FilmsViewSet(viewsets.ModelViewSet):

    serializer_class = FilmSerializer

    @staticmethod
    def get_queryset():
        #check_if_empty_films()
        return Film.objects.all()


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer

    @staticmethod
    def get_queryset():
        return Staff.objects.all()

    # action_to_serializer = {
    #     "list": FilmStaffListRetrieveSerializer,
    #     "retrieve":FilmStaffListRetrieveSerializer,
    # }
    #
    # def get_serializer_class(self):
    #     return self.action_to_serializer.get(
    #         self.action,
    #         self.serializer_class
    #     )
