from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import FieldError
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Max, Min, Sum
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

    @action(detail = False)
    def get_labels(self, request):
        data = None
        label = self.request.query_params.get('label', None)
        if label is not None:
            try:
                data = self.queryset.order_by(label).values_list(
                    label, 
                    flat = True
                ).distinct()

                if label == 'year' and len(data) > 0:
                    data = self.queryset.order_by('year').values_list('year', flat=True).aggregate(Min('year'), Max('year'))
            except FieldError as error:
                return Response(
                    {"message" : "Field error, use only gender, year, age or disease_name"},
                    status = status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'labels' : data},
            status = status.HTTP_200_OK
        )

    @action(detail = False)
    def get_line_chart(self, request):
        filtered_queryset = self.filter_queryset(self.queryset)

        data = filtered_queryset.values('region__name', 'year') \
            .order_by('year') \
            .annotate(year_value = Sum('value'))

        return Response(
            {'data': data},
            status = status.HTTP_200_OK
        )
    
    @action(detail = False)
    def get_bar_chart(self, request):
        filtered_queryset = self.filter_queryset(self.queryset)

        data = filtered_queryset.values('region__name', 'value') \
            .order_by('value') \
            .annotate(region_value = Sum('value')) \
            .order_by('-region__name')

        return Response(
            {'data': data},
            status = status.HTTP_200_OK
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

    @action(detail = False)
    def get_labels(self, request):
        data = None
        label = self.request.query_params.get('label', None)
        if label is not None:
            try:
                data = self.queryset.order_by(label).values_list(
                    label, 
                    flat = True
                ).distinct()

                if label == 'year' and len(data) > 0:
                    data = self.queryset.order_by('year').values_list('year', flat=True).aggregate(Min('year'), Max('year'))
            except FieldError as error:
                return Response(
                    {"message" : "Field error, use only disease, gender, standard or year"},
                    status = status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'labels' : data},
            status = status.HTTP_200_OK
        )

    @action(detail = False)
    def get_line_chart(self, request):
        filtered_queryset = self.filter_queryset(self.queryset)

        data = filtered_queryset.values('year') \
            .order_by('year') \
            .annotate(preventive_value = Sum('preventive')) \
            .annotate(curable_value = Sum('curable')) \
            .annotate(preventable_value = Sum('preventable'))

        return Response(
            {'data': data},
            status = status.HTTP_200_OK
        )
    
    @action(detail = False)
    def get_bar_chart(self, request):
        filtered_queryset = self.filter_queryset(self.queryset)

        data = filtered_queryset.values('region__name') \
            .order_by('region__name') \
            .annotate(preventive_value = Sum('preventive')) \
            .annotate(curable_value = Sum('curable')) \
            .annotate(preventable_value = Sum('preventable'))

        return Response(
            {'data': data},
            status = status.HTTP_200_OK
        )

    #TO-DO create separate action for heatmap