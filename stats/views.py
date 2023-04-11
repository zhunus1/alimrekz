from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.decorators import action

from .models import (
    DiseaseGroup,
    Region,
    DeathStatistic,
    PreventStatistic
)
from .serializers import (
    DeathStatisticSerializer,
    PreventStatisticSerializer,
    DiseaseGroupSerializer,
    RegionSerializer,
)


class DiseaseGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiseaseGroup.objects.all()
    serializer_class = DiseaseGroupSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DeathStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeathStatistic.objects.select_related(
        'region',
        'group'
    ).all()
    serializer_class = DeathStatisticSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = (
        'region',
        'disease_name',
        'age',
        'gender',
        'group',
        'year'
    )



class PreventStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PreventStatistic.objects.select_related(
        'region',
    ).all()
    serializer_class = PreventStatisticSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = (
        'region',
        'disease',
        'gender',
        'standard',
        'year'
    )

    #TO-DO create separate action for heatmap
