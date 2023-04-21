from django.shortcuts import render
from rest_framework import viewsets, status, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.core.exceptions import FieldError
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import action
import io
import pandas as pd
import seaborn as sns
import matplotlib
import matplotlib.pyplot as plt
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
    PreventBarChartSerializer,
    PreventLineChartSerializer,
    DeathLineChartSerializer,
    DeathBarChartSerializer
)


class DiseaseGroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiseaseGroup.objects.all()
    serializer_class = DiseaseGroupSerializer


class RegionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class DeathStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = DeathStatisticSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = (
        'region__name',
        'disease_name',
        'age',
        'gender',
        'group__name',
        'year'
    )

    def get_queryset(self):
        queryset = DeathStatistic.objects.select_related(
            'region',
            'group'
        ).all()

        regions = self.request.query_params.get('regions', None)
        groups = self.request.query_params.get('groups', None)

        if regions is not None:
            queryset = queryset.filter(region__name__in = regions.split(','))

        if groups is not None:
            queryset = queryset.filter(group__name__in = groups.split(','))

        return queryset

    @action(detail = False)
    def get_labels(self, request):
        data = None
        label = self.request.query_params.get('label', None)
        if label is not None:
            try:
                data = self.get_queryset().order_by(label).values_list(
                    label, 
                    flat = True
                ).distinct()

                if label == 'year' and len(data) > 0:
                    data = self.get_queryset().order_by('year').values_list('year', flat=True).aggregate(Min('year'), Max('year'))
                if label == 'region' and len(data) > 0:
                    data = self.get_queryset().order_by('region').values_list('region__name', flat=True).distinct()
                if label == 'group' and len(data) > 0:
                    data = self.get_queryset().order_by('group').values_list('group__name', flat=True).distinct()
            except FieldError as error:
                return Response(
                    {"message" : "Field error, use only gender, year, region, age or disease_name"},
                    status = status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'labels' : data},
            status = status.HTTP_200_OK
        )

    @action(detail = False)
    def get_line_chart(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())

        data = filtered_queryset.values('year') \
            .order_by('year') \
            .annotate(year_total_value = Sum('value'))

        page = self.paginate_queryset(data)

        if page is not None:
            serializer = DeathLineChartSerializer(
                page, 
                context = {
                    'queryset': filtered_queryset
                },
                many=True
            )
            return self.get_paginated_response(serializer.data)
        
    
    @action(detail = False)
    def get_bar_chart(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())

        data = filtered_queryset.values('region__name') \
            .order_by('region__name') \
            .annotate(region_value_total = Sum('value'))

        page = self.paginate_queryset(data)

        if page is not None:
            serializer = DeathBarChartSerializer(
                page, 
                context = {
                    'queryset': filtered_queryset
                },
                many=True
            )
            return self.get_paginated_response(serializer.data)


class PreventStatisticViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = PreventStatisticSerializer
    filter_backends = (
        DjangoFilterBackend,
    )
    filterset_fields = (
        'region__name',
        'disease',
        'gender',
        'standard',
        'year'
    )

    def get_queryset(self):
        queryset = PreventStatistic.objects.select_related(
            'region',
        ).all()

        regions = self.request.query_params.get('regions', None)
        diseases = self.request.query_params.get('diseases', None)

        if regions is not None:
            queryset = queryset.filter(region__name__in = regions.split(','))

        if diseases is not None:
            queryset = queryset.filter(disease__in = diseases.split(','))

        return queryset

    @action(detail = False)
    def get_labels(self, request):
        data = None
        label = self.request.query_params.get('label', None)
        if label is not None:
            try:
                data = self.get_queryset().order_by(label).values_list(
                    label, 
                    flat = True
                ).distinct()

                if label == 'year' and len(data) > 0:
                    data = self.get_queryset().order_by('year').values_list('year', flat=True).aggregate(Min('year'), Max('year'))
                if label == 'region' and len(data) > 0:
                    data = self.get_queryset().order_by('region').values_list('region__name', flat=True).distinct()
            except FieldError as error:
                return Response(
                    {"message" : "Field error, use only disease, gender, region, standard or year"},
                    status = status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'labels' : data},
            status = status.HTTP_200_OK
        )

    @action(detail = False)
    def get_line_chart(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())

        data = filtered_queryset.values('year') \
            .order_by('year') \
            .annotate(year_preventive_total = Sum('preventive')) \
            .annotate(year_curable_total = Sum('curable')) \
            .annotate(year_preventable_total = Sum('preventable'))

        page = self.paginate_queryset(data)

        if page is not None:
            serializer = PreventLineChartSerializer(
                page, 
                context = {
                    'queryset': filtered_queryset
                },
                many=True
            )
            return self.get_paginated_response(serializer.data)
    
    @action(detail = False)
    def get_bar_chart(self, request):
        filtered_queryset = self.filter_queryset(self.get_queryset())

        data = filtered_queryset.values('region__name') \
            .order_by('region__name') \
            .annotate(disease_preventive_total = Sum('preventive')) \
            .annotate(disease_curable_total = Sum('curable')) \
            .annotate(disease_preventable_total = Sum('preventable'))

        page = self.paginate_queryset(data)

        if page is not None:
            serializer = PreventBarChartSerializer(
                page, 
                context = {
                    'queryset': filtered_queryset
                },
                many=True
            )
            return self.get_paginated_response(serializer.data)

    @action(detail = False)
    def get_heatmap(self, request):
        data = None
        queryset = self.filter_queryset(self.get_queryset())
        type = self.request.query_params.get('type', None)
        
        if type is not None:
            try:
                queryset = queryset.values_list(
                    "disease",
                    "region__name",
                    type
                )

                df = pd.DataFrame(
                    list(queryset), 
                    columns = (
                        "disease",
                        "region",
                        type
                    )
                )

                table = pd.pivot_table(
                    df, 
                    values = type, 
                    index = ["disease"], 
                    columns = ["region"], 
                    fill_value = 0
                )
            
                regions = table.columns.tolist()
                diseases = table.index.unique().tolist()
                values = []
        
                for index, row in table.iterrows():
                    values.append(row.values.tolist())
                
                data = {
                    'regions': regions,
                    'diseases': diseases,
                    'values': values,
                }

            except FieldError as error:
                return Response(
                    {"message" : "Field error, use only curable, preventable or preventive"},
                    status = status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {
                "data" : data
            },
            status = status.HTTP_200_OK
        )