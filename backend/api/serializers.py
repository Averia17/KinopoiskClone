from rest_framework.serializers import ModelSerializer

from backend.models import Film


class FilmSerializer(ModelSerializer):
    class Meta:
        model = Film
        fields = ['__all__']