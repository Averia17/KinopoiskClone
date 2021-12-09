from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q
from django_filters import rest_framework as filters
from kinopoiskclone.models import Film


class MultiValueCharFilter(filters.BaseCSVFilter, filters.CharFilter):
    def filter(self, qs, value):
        # value is either a list or an 'empty' value
        values = value or []

        for value in values:
            qs = super(MultiValueCharFilter, self).filter(qs, value)

        return qs


class FilmSearchFilter(filters.FilterSet):
    name = filters.CharFilter(field_name='name', method='full_text_search')
    min_rating = filters.CharFilter(field_name="rating", method='great_than')
    max_rating = filters.CharFilter(field_name="rating", method='less_than')
    min_year = filters.CharFilter(field_name="year", method='great_than')
    max_year = filters.CharFilter(field_name="year", method='less_than')
    genres__title = MultiValueCharFilter(field_name="genres__title",  lookup_expr='contains')
    countries__title = filters.CharFilter(field_name="countries__title", lookup_expr='contains')

    def full_text_search(self, queryset, value, *args):
        search_query = SearchQuery(value)
        qs = queryset.annotate(
            rank=SearchRank(F('vector_name'), search_query),
            similarity=TrigramSimilarity(value, args[0])
            # similarity=TrigramSimilarity('name', query) + TrigramSimilarity('description', query)
        ).filter(Q(rank__gte=0.2) | Q(similarity__gt=0.2)).order_by('-similarity')
        # queryset = Film.objects.filter(pk__in=[
        #     i.id for i in Film.objects.raw(f"SELECT * FROM search_movies_by_name('{args[0]}')")
        # ])
        # return queryset
        return qs.distinct('id', 'name', 'year', 'image', 'similarity').values_list(
            'id', 'name', 'year', 'image', 'genres__title', 'similarity', named=True
        )

    def great_than(self, queryset, value, *args):
        filter_parameter = {value + '__gte': args[0]}
        queryset = queryset.filter(**filter_parameter)
        return queryset.distinct('id', 'name', 'year', 'image').values_list(
            'id', 'name', 'year', 'image', 'genres__title', named=True
        )

    def less_than(self, queryset, value, *args):
        filter_parameter = {value + '__lte': args[0]}
        queryset = queryset.filter(**filter_parameter)
        return queryset.distinct('id', 'name', 'year', 'image').values_list(
            'id', 'name', 'year', 'image', 'genres__title', named=True
        )

    class Meta:
        model = Film
        fields = ('name', 'min_rating', 'max_rating', 'min_year', 'max_year', 'genres__title', 'countries__title')


class FilmFormFilter(filters.FilterSet):
    pass
