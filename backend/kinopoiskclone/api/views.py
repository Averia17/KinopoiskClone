from django.core.exceptions import ObjectDoesNotExist
from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kinopoiskclone.models import Film, Staff, Country, Genre, UserProfile
from .serializers import StaffSerializer, FilmSerializer, GenreSerializer, \
    CountrySerializer, FilmListSerpySerializer, StaffListSerpySerializer, UserProfileSerializer, FilmListSerializer
from .services import serialize_value_list_films, delete_saved_users_film


class FilmsViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    # lookup_field = 'slug'
    queryset = Film.objects.filter(type='FILM').prefetch_related('genres')
    http_method_names = ['get', 'head', 'options', 'post']

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


class SerialsViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    http_method_names = ['get', 'head', 'options', 'post']

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
    http_method_names = ['get', 'head', 'options']

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
    http_method_names = ['get', 'head', 'options']

    def retrieve(self, request, *args, **kwargs):
        queryset = Film.objects.filter(genres__slug=kwargs['slug']).prefetch_related('genres')
        serializer = serialize_value_list_films(queryset)
        return Response(serializer.data)


class CountriesViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'slug'
    http_method_names = ['get', 'head', 'options']

    def retrieve(self, request, *args, **kwargs):
        queryset = Film.objects.filter(countries__slug=kwargs['slug']).prefetch_related('countries')
        serializer = serialize_value_list_films(queryset)
        return Response(serializer.data)


class AllMoviesViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    # lookup_field = 'slug'
    http_method_names = ['get', 'head', 'options']

    filter_backends = (SearchFilter, OrderingFilter)
    search_fields = ('name', 'year', 'genres__title')
    queryset = Film.objects.prefetch_related('genres')

    action_to_serializer = {
        "list": FilmListSerializer,
        "retrieve": FilmSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all().prefetch_related('saved_films')
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head', 'options', 'delete']


class FavoritesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FilmListSerializer

    def get_queryset(self):
        saved_films = self.request.user.userprofile.saved_films
        return saved_films

    def create(self, request, *args, **kwargs):
        userprofile = self.request.user.userprofile
        pk = self.request.data.get('id')
        film = Film.objects.get(pk=pk)
        userprofile.saved_films.add(film)
        serializer = serialize_value_list_films(userprofile.saved_films)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            userprofile = self.request.user.userprofile
            saved_films = delete_saved_users_film(userprofile, pk)
            serializer = serialize_value_list_films(saved_films)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.data)
