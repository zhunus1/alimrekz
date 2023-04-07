from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import (
    DiseaseGroup,
    Region,
    DeathStatistic,
    PreventStatistic
)
from .serializers import (
    DeathStatisticSerializer,
    PreventStatisticSerializer
)

# Create your views here.
#TO-DO:Filters for both API
#TO-DO: Override get_queryset with select_related

class DeathStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DeathStatistic.objects.select_related(
        'region',
        'group'
    ).all()
    serializer_class = DeathStatisticSerializer

class PreventStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PreventStatistic.objects.select_related(
        'region',
    ).all()
    serializer_class = PreventStatisticSerializer