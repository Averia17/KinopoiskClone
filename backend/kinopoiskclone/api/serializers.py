import serpy
from rest_framework.serializers import ModelSerializer

from ..models import Film, Staff, Country, Genre


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
    title = serpy.Field(required=False)

# class GenreNameSerializer(serpy.Serializer):
#
#     class Meta:
#         model = Genre
#         fields = ('title',)


class FilmListSerializer(ModelSerializer):

    genres = GenreNameSerializer(many=True)

    class Meta:
        model = Film
        fields = ('id', 'name', 'image', 'year', 'genres')
        read_only_fields = fields


class FilmListSerpySerializer(serpy.Serializer):
    id = serpy.IntField()
    name = serpy.Field(required=False)
    image = serpy.Field(required=False)
    year = serpy.Field(required=False)
    genres = GenreNameSerializer(many=True, attr="genres.all", call=True) #attr="groups.all", call=True

    #genres = serpy.MethodField(required=False)

    # @staticmethod
    # def get_genres(self, obj):
    #     #print(obj.genres.first())
    #     #return GenreNameSerializer(obj.genres.first()).data
    #     return obj.genres.all()
    # class Meta:
    #     model = Film
    #     fields = ('id', 'name', 'image', 'year', 'genres')
    #     read_only_fields = fields

