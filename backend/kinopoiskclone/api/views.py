from django.contrib.postgres.search import TrigramSimilarity, SearchRank, SearchQuery, SearchVector, TrigramDistance
from django.core.exceptions import ObjectDoesNotExist, FieldError
from django.db.models import Value, Q, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated

from kinopoiskclone.models import Film, Staff, Country, Genre, User
from .filters import FilmSearchFilter
from .serializers import StaffSerializer, FilmSerializer, GenreSerializer, \
    CountrySerializer, FilmListSerpySerializer, StaffListSerpySerializer, UserProfileSerializer, FilmListSerializer, \
    UserRegisterSerializer
from .services import serialize_value_list_films, delete_saved_users_film


from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer


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
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all().prefetch_related('saved_films')
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'head', 'options', 'delete']


class FavoritesViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    serializer_class = FilmListSerializer

    def get_queryset(self):
        saved_films = self.request.user.saved_films
        return saved_films

    def create(self, request, *args, **kwargs):
        userprofile = self.request.user
        pk = self.request.data.get('id')
        film = Film.objects.get(pk=pk)
        userprofile.saved_films.add(film)
        serializer = serialize_value_list_films(userprofile.saved_films)
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        try:
            userprofile = self.request.user
            saved_films = delete_saved_users_film(userprofile, pk)
            serializer = serialize_value_list_films(saved_films)
        except ObjectDoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.data)
