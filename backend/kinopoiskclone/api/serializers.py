import serpy
from kinopoiskclone.models import User
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, CharField
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from ..models import Film, Staff, Country, Genre


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(min_length=8)

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["email"], validated_data["password"]
        )
        return user

    class Meta:
        model = User
        fields = ("id", "email", "password")


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class GenreSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class StaffListSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = ('id', 'nameRu', 'professionKey', 'professionText')


class StaffListSerpySerializer(serpy.Serializer):
    id = serpy.IntField()
    nameRu = serpy.Field(required=False)
    professionKey = serpy.Field(required=False)
    professionText = serpy.Field(required=False)


class FilmSerializer(ModelSerializer):
    staff = StaffListSerializer(many=True)  # attr="groups.all", call=True
    genres = GenreSerializer(many=True)
    countries = CountrySerializer(many=True)

    class Meta:
        model = Film
        fields = '__all__'


class GenreNameSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title',)


class FilmListSerializer(ModelSerializer):
    genres__title = CharField(source='genres.first', max_length=1024, required=False)

    class Meta:
        model = Film
        fields = ('id', 'name', 'image', 'year', 'type', 'genres__title')
        read_only_fields = fields


class FilmListSerpySerializer(serpy.Serializer):
    id = serpy.IntField()
    name = serpy.Field(required=False)
    image = serpy.Field(required=False)
    year = serpy.Field(required=False)
    type = serpy.Field(required=False)
    distance = serpy.Field(required=False)
    genres__title = serpy.Field(required=False)


class GenreSeprySerializer(serpy.Serializer):
    id = serpy.IntField()
    title = serpy.Field()


class FilmFullListSerpySerializer(serpy.Serializer):
    id = serpy.IntField()
    name = serpy.Field(required=False)
    image = serpy.Field(required=False)
    year = serpy.Field(required=False)
    type = serpy.Field(required=False)
    genres = GenreSeprySerializer(many=True, call=True, attr='genres.all')


class UserSerializer(ModelSerializer):
    saved_films = FilmListSerializer(many=True, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'saved_films')


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super(CustomTokenObtainPairSerializer, self).validate(attrs)
        # Custom data you want to include
        data.update({'id': self.user.id})
        return data
