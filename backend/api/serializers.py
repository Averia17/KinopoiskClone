import serpy
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
        fields = ('id', 'nameRu', 'professionKey', 'professionText')


class FilmSerializer(ModelSerializer):

    staff = StaffListSerializer(many=True)
    genres = GenreSerializer(many=True)
    countries = CountrySerializer(many=True)

    class Meta:
        model = Film
        fields = '__all__'


class GenreNameSerializer(serpy.Serializer):
    title = serpy.Field()



class FilmListSerializer(ModelSerializer):

    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Film
        fields = ('id', 'name', 'image', 'year', 'genres')
        read_only_fields = fields




class FilmListSerpySerializer(serpy.Serializer):
    #genres = GenreNameSerializer(many=True, attr="genres.all", call=True) #attr="groups.all", call=True

    id = serpy.IntField()
    name = serpy.Field(required=False)
    image = serpy.Field(required=False)
    year = serpy.Field(required=False)
    # class Meta:
    #     model = Film
    #     fields = ('id', 'name', 'image', 'year', 'genres')
    #     read_only_fields = fields

