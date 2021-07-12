from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from backend.models import Film, Staff


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

    class Meta:
        model = Film
        fields = '__all__'


class FilmListSerializer(ModelSerializer):

    class Meta:
        model = Film
        fields = ('id', 'name', 'image', 'year')

