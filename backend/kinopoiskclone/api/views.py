from django.contrib.postgres.search import TrigramSimilarity, SearchRank, SearchQuery, SearchVector, TrigramDistance
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db.models import Value, Q, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from django.db import connection
from rest_framework_simplejwt.views import TokenObtainPairView
from kinopoiskclone.models import Film, Staff, Country, Genre, User
from .filters import FilmSearchFilter
from .serializers import StaffSerializer, FilmSerializer, GenreSerializer, \
    CountrySerializer, FilmListSerpySerializer, StaffListSerpySerializer, UserSerializer, FilmListSerializer, \
    UserRegisterSerializer, CustomTokenObtainPairSerializer
from .services import serialize_value_list_films, delete_saved_users_film

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView


class RegisterUser(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception:
                return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)


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
        #queryset = serialize_value_list_films(self.queryset)
        queryset = Film.objects.raw("SELECT * FROM select_movies_by_type('FILM')")

        serializer = FilmListSerpySerializer(queryset, many=True)
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
        # queryset = serialize_value_list_films(self.queryset)
        queryset = Film.objects.raw("SELECT * FROM select_movies_by_type('TV_SHOW')")
        serializer = FilmListSerpySerializer(queryset, many=True)
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
        # queryset = Film.objects.filter(genres__slug=kwargs['slug']).prefetch_related('genres')
        # queryset = serialize_value_list_films(queryset)
        queryset = Film.objects.raw(f"SELECT * FROM select_movies_by_genre('{kwargs['slug']}')")
        serializer = FilmListSerpySerializer(queryset, many=True)
        return Response(serializer.data)


class CountriesViewSet(viewsets.ModelViewSet):
    serializer_class = CountrySerializer
    queryset = Country.objects.all()
    lookup_field = 'slug'
    http_method_names = ['get', 'head', 'options']

    def retrieve(self, request, *args, **kwargs):
        # queryset = Film.objects.filter(countries__slug=kwargs['slug']).prefetch_related('countries')
        # queryset = serialize_value_list_films(queryset)
        queryset = Film.objects.raw(f"SELECT * FROM select_movies_by_country('{kwargs['slug']}')")
        serializer = FilmListSerpySerializer(queryset, many=True)
        return Response(serializer.data)


class AllMoviesViewSet(viewsets.ModelViewSet):
    serializer_class = FilmSerializer
    # lookup_field = 'slug'
    http_method_names = ['get', 'head', 'options']
    filter_backends = (DjangoFilterBackend,)
    filter_class = FilmSearchFilter
    # search_fields = ('name', 'year', 'genres__title')
    queryset = Film.objects.all().prefetch_related('genres')

    action_to_serializer = {
        "list": FilmListSerpySerializer,
        "retrieve": FilmSerializer,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )

    def list(self, request):
        if len(request.query_params) > 0:
            queryset = self.filter_queryset(self.get_queryset())
        else:
            queryset = serialize_value_list_films(self.queryset)
        serializer = FilmListSerpySerializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all().prefetch_related('saved_films')
    # permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head', 'options', 'delete']


class FavoritesViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAuthenticated,)
    serializer_class = FilmListSerializer

    def get_permissions(self):
        return [
            permission()
            for permission in self.permission_to_method.get(
                self.action, self.permission_classes
            )
        ]

    permission_to_method = {
        "create": [IsAuthenticated],
    }

    def get_queryset(self):
        user = self.request.user
        saved_films = User.saved_films.through.objects.none()
        if not user.is_anonymous:
            saved_films = user.saved_films
        return saved_films

    def create(self, request, *args, **kwargs):
        user = self.request.user
        pk = self.request.data.get('id')
        # film = Film.objects.get(pk=pk)
        # user.saved_films.add(film)
        # queryset = serialize_value_list_films(user.saved_films)
        queryset = Film.objects.raw(f"SELECT * FROM insert_saved_film({user.pk}, {pk})")
        serializer = FilmListSerpySerializer(queryset, many=True)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            user = self.request.user
            # saved_films = delete_saved_users_film(user, pk)
            # queryset = serialize_value_list_films(saved_films)
            queryset = Film.objects.raw(f"SELECT * FROM delete_saved_film({user.pk}, {pk})")
            serializer = FilmListSerpySerializer(queryset, many=True)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        user = User.objects.get(pk=kwargs['pk'])
        queryset = user.saved_films.all()
        serializer = FilmListSerpySerializer(queryset, many=True)
        # favorites_ids = user.saved_films.values_list('id', flat=True)
        return Response(serializer.data)


class CustomTokenObtainPairView(TokenObtainPairView):
    # Replace the serializer with your custom
    serializer_class = CustomTokenObtainPairSerializer
