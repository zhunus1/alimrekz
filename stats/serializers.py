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
            'disease_name',
            'value',
        )


class PreventStatisticSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source="region.name")
    class Meta:
        model = PreventStatistic
        fields = (
            'region',
            'preventive',
            'curable',
            'preventable',
        )


class PreventBarChartSerializer(serializers.ModelSerializer):
    disease_preventive_total = serializers.FloatField()
    disease_curable_total = serializers.FloatField()
    disease_preventable_total = serializers.FloatField()
    regions = serializers.SerializerMethodField()

    def get_regions(self, obj):

        return PreventStatisticSerializer(
            self.context['queryset'].filter(
                disease = obj['disease'],
            ), 
            many = True
            ).data


    class Meta:
        model = PreventStatistic
        fields = (
            'disease',
            'disease_preventive_total',
            'disease_curable_total',
            'disease_preventable_total',
            'regions'
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