from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from backend.models import Film


# class FilmSerializer(ModelSerializer):
#     class Meta:
#         model = Film
#         fields = ('name', 'year', 'rating', 'image')


class FilmSerializer(serializers.Serializer):
    nameRu = serializers.CharField(max_length=100)
    year = serializers.CharField(max_length=4)
    rating = serializers.CharField(max_length=5)
    posterUrl = serializers.CharField(max_length=255)