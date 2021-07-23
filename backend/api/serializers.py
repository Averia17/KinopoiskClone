from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from backend.models import Film, Staff, Country, Genre



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
        fields = ('id', 'nameRu', 'professionKey')


class FilmSerializer(ModelSerializer):

    staff = StaffListSerializer(many=True)
    genres = GenreSerializer(many=True)
    countries = CountrySerializer(many=True)

    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(ModelSerializer):

    genres = GenreSerializer(many=True)

    class Meta:
        model = Film
        fields = ('id', 'name', 'image', 'year', 'genres', 'type')


