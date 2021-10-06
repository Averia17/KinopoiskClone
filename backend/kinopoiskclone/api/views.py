from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response

from kinopoiskclone.models import Film, Staff, Country, Genre
from .serializers import StaffSerializer, FilmSerializer, GenreSerializer, \
    CountrySerializer, FilmListSerpySerializer, StaffListSerpySerializer
from .services import serialize_value_list_films


class FilmsViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    # lookup_field = 'slug'
    queryset = Film.objects.filter(type='FILM').prefetch_related('genres')

    action_to_serializer = {
        "retrieve": FilmSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )
    #
    # def retrieve(self, *args, **kwargs):
    #     return super(FilmsViewSet, self).retrieve(*args, **kwargs)
    #
    def list(self, request):
        serializer = serialize_value_list_films(self.queryset)

        return Response(serializer.data)


class SerialsViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer

    queryset = Film.objects.filter(type='TV_SHOW').prefetch_related('genres')

    action_to_serializer = {
        "retrieve": FilmSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )

    def list(self, request):
        serializer = serialize_value_list_films(self.queryset)
        return Response(serializer.data)


class StaffViewSet(viewsets.ModelViewSet):
    serializer_class = StaffSerializer
    queryset = Staff.objects.all()

    action_to_serializer = {
        "list": StaffListSerpySerializer,
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
        queryset = Film.objects.filter(genres__slug=kwargs['slug']).prefetch_related('genres')
        serializer = serialize_value_list_films(queryset)
        return Response(serializer.data)


class CountriesViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'slug'

    def retrieve(self, request, *args, **kwargs):
        queryset = Film.objects.filter(countries__slug=kwargs['slug']).prefetch_related('countries')
        serializer = serialize_value_list_films(queryset)
        return Response(serializer.data)


class AllMoviesViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    # lookup_field = 'slug'

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'year', 'genres__title')
    queryset = Film.objects.order_by('-rating').prefetch_related('genres')

    action_to_serializer = {
        "list": FilmListSerpySerializer,
        "retrieve": FilmSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )
