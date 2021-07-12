from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from backend.models import Film, Staff


class StaffSerializer(ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class FilmSerializer(ModelSerializer):

    staff = StaffSerializer(many=True)

    class Meta:
        model = Film
        fields = '__all__'
