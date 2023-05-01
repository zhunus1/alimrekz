from django_filters import rest_framework as filters
from .models import DeathStatistic

class NumberInFilter(filters.BaseInFilter, filters.NumberFilter):
    pass

class DeathFilterBackend(filters.FilterSet):
    regions = NumberInFilter(field_name='region', lookup_expr='in')
    groups = NumberInFilter(field_name='disease__group', lookup_expr='in')
    diseases = NumberInFilter(field_name='disease', lookup_expr='in')
    class Meta:
        model = DeathStatistic
        fields = (
            'regions',
            'groups',
            'diseases',
            'region',
            'disease',
            'age',
            'gender',
            'year'
        )