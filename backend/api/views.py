from django.core.cache import cache
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.views import APIView

from .serializers import FilmListSerializer, StaffSerializer, FilmSerializer, StaffListSerializer, GenreSerializer, \
    CountrySerializer, FilmListSerpySerializer
from ..models import Film, Staff, Genre, Country
from .services import check_if_empty_films


class FilmsViewSet(viewsets.ViewSet):
    #serializer_class = FilmListSerpySerializer
    # lookup_field = 'slug'
    #queryset = Film.objects.filter(type='FILM').order_by('-rating')

    def list(self, request):
        queryset = Film.objects.filter(type='FILM').\
            order_by('-rating').values_list('id', 'image', 'name', 'year', 'genres__title', named=True)
        # for item in queryset:
        # for item in queryset:
        #     print(item)
        #     print(getattr(item.genres.first(), 'title', None))
        serializer = FilmListSerpySerializer(queryset, many=True)
        #print(serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        film = Film.objects.get(pk=pk)
        serializer = FilmSerializer(film)
        return Response(serializer.data)
    # @staticmethod
    # def get_queryset():
    #     # data = cache.get('films')
    #     # if data is None:
    #     #     films = Film.objects.filter(type='FILM').order_by('-rating')
    #     #     serializer = FilmListSerializer(films)
    #     #     data = serializer.data
    #     #     cache.set('films', films, 86400)
    #     # print(data)
    #     # check_if_empty_films()
    #     # Полная дичь но слайсы нельзя делать...
    #     # n = 0
    #     # films = []
    #     # for film in Film.objects.filter(type='FILM').order_by('-rating'):
    #     #     if n == 50:
    #     #         return films
    #     #     films.append(film)
    #     #
    #     #     n += 1
    #
    #     return Film.objects.filter(type='FILM').order_by('-rating') # Film.objects.filter(type='FILM').order_by('-rating')


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
        # check_if_empty_films()
        # Полная дичь но слайсы нельзя делать...
        # n = 0
        # films = []
        # for film in Film.objects.filter(type='TV_SHOW').order_by('-rating'):
        #     if n == 50:
        #         return films
        #     films.append(film)
        #
        #     n += 1
        # Film.objects.filter(type='TV_SHOW').order_by('-rating')
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


class GenresViewSet(viewsets.ModelViewSet):
    lookup_field = 'slug'
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

    def retrieve(self, request, *args, **kwargs):
        queryset = Film.objects.filter(genres__slug=kwargs['slug'])
        serializer = FilmListSerializer(queryset, many=True)
        return Response(serializer.data)


class CountriesViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        queryset = Film.objects.filter(countries__slug=kwargs['slug'])
        serializer = FilmListSerializer(queryset, many=True)
        return Response(serializer.data)
