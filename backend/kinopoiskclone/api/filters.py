import django_filters

from kinopoiskclone.models import Film


class FilmFilter(django_filters.FilterSet):
    genres = django_filters.CharFilter(
        name='genres__title',
        lookup_type='contains',
    )
    countries = django_filters.CharFilter(
        name='countries__title',
        lookup_type='contains',
    )

    class Meta:
        model = Film
        fields = ('genres', 'countries')
