from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from backend.models import Film


class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        fields = ('name', 'year', 'rating', 'image', 'filmId')


