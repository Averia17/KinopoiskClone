from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from django.db.models import F, Q
from django_filters import rest_framework as filters

from kinopoiskclone.models import Film


class FilmFilter(filters.FilterSet):
    name = filters.CharFilter(
        field_name='name',
        method='full_text_search',
    )

    def full_text_search(self, queryset, value, *args):
        search_query = SearchQuery(value, config='russian')
        qs = queryset.annotate(
            rank=SearchRank(F('vector_name'), search_query),
            similarity=TrigramSimilarity(value, args[0])
            # similarity=TrigramSimilarity('name', query) + TrigramSimilarity('description', query)
        ).filter(Q(rank__gte=0.2) | Q(similarity__gt=0.2)).order_by('-similarity')

        return qs.distinct('id', 'name', 'year', 'image', 'similarity').values_list(
            'id', 'name', 'year', 'image', 'genres__title', 'similarity', named=True
        )
