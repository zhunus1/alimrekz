from rest_framework import serializers
from django.db.models import Max, Min, Sum
from .models import (
    DiseaseGroup,
    Region,
    DeathStatistic,
    PreventStatistic
)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = (
            'id',
            'name',
        )


class DiseaseGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiseaseGroup
        fields = (
            'id',
            'name',
        )


class DeathStatisticSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    group = DiseaseGroupSerializer()
    class Meta:
        model = DeathStatistic
        fields = (
            'region',
            'group',
            'year',
            'age',
            'gender',
            'disease_name',
            'value',
        )


class PreventStatisticSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    class Meta:
        model = PreventStatistic
        fields = (
            'region',
            'year',
            'disease',
            'standard',
            'gender',
            'preventive',
            'curable',
            'preventable',
        )


class PreventStatisticBarChartSerializer(serializers.ModelSerializer):
    preventive_total = serializers.FloatField()
    curable_total = serializers.FloatField()
    preventable_total = serializers.FloatField()
    class Meta:
        model = PreventStatistic
        fields = (
            'disease',
            'preventive_total',
            'curable_total',
            'preventable_total',
        )


class PreventBarChartSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    disease_preventive_total = serializers.FloatField()
    disease_curable_total = serializers.FloatField()
    disease_preventable_total = serializers.FloatField()
    diseases = serializers.SerializerMethodField()

    def get_diseases(self, obj):

        return PreventStatisticBarChartSerializer(
            self.context['queryset'].filter(
                region__name = obj['region__name'],
            ).values('disease') \
            .order_by('disease') \
            .annotate(preventive_total = Sum('preventive')) \
            .annotate(curable_total = Sum('curable')) \
            .annotate(preventable_total = Sum('preventable')),
            many = True
            ).data


    class Meta:
        model = PreventStatistic
        fields = (
            'region',
            'disease_preventive_total',
            'disease_curable_total',
            'disease_preventable_total',
            'diseases'
        )


class PreventStatisticLineChartSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreventStatistic
        fields = (
            'disease',
            'preventive',
            'curable',
            'preventable',
        )


class PreventLineChartSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    region_preventive_total = serializers.FloatField()
    region_curable_total = serializers.FloatField()
    region_preventable_total = serializers.FloatField()
    years = serializers.SerializerMethodField()

    def get_years(self, obj):

        return PreventStatisticLineChartSerializer(
            self.context['queryset'].filter(
                region__name = obj['region__name'],
            ), 
            many = True
            ).data


    class Meta:
        model = PreventStatistic
        fields = (
            'region',
            'region_preventive_total',
            'region_curable_total',
            'region_preventable_total',
            'years'
        )