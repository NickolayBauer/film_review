from functools import reduce

from django import forms
from django.contrib.postgres.search import SearchVector
from django.db.models import Count
from django.db.models import Q
from django_select2.forms import ModelSelect2MultipleWidget

import django_filters
import operator

from .models import Film
from .models import Genre


class FilmFilter(django_filters.FilterSet):
    class Meta:
        model = Film
        fields = (
            'title',
            'description',
            'genres',
            'budget'
        )

    keywords = django_filters.CharFilter(method='kw_filter', label='Ключевые слова')

    def kw_filter(self, queryset, name, value):
        vector = reduce(operator.and_, (Q(search=value) for value in value.split()))
        return queryset.annotate(search=SearchVector('title', 'description')).filter(vector)

    year = django_filters.NumberFilter(method='year_filter', label='Год')

    def year_filter(self, queryset, name, value):
        return queryset.filter(year=value)

    order = django_filters.OrderingFilter(
        choices=(
            ('title', 'По названию'),
            ('-year', 'По дате (сначала новые)'),
            ('year', 'По дате (сначала старые)'),
        ),
        fields={
            'title': 'title',
            'year': 'year',
        },
    )

    genres = django_filters.ModelMultipleChoiceFilter(
        widget=ModelSelect2MultipleWidget(
            queryset=Genre.objects.order_by('name'),
            search_fields=['name__icontains'],
            max_results=10,
            required=False,
            attrs={'data-language': 'ru'}
        ),
        label='Жанры',
        queryset=Genre.objects.all()
    )
