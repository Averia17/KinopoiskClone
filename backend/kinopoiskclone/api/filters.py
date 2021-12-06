from django_filters import rest_framework as filters

from kinopoiskclone.models import Film


class FilmFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='icontains',
    )

    class Meta:
        model = Film
        fields = ('name', )
