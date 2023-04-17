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


class DeathStatisticLineChartSerializer(serializers.ModelSerializer): 
    region = serializers.CharField(source='region__name')
    value_total = serializers.FloatField()
    class Meta:
        model = DeathStatistic
        fields = (
            'region',
            'value_total',
        )


class DeathLineChartSerializer(serializers.ModelSerializer):
    year = serializers.CharField()
    year_total_value = serializers.FloatField()
    regions = serializers.SerializerMethodField()

    def get_regions(self, obj):

        return DeathStatisticLineChartSerializer(
            self.context['queryset'].filter(
                year = obj['year'],
            ).values('region__name') \
            .order_by('region__name') \
            .annotate(value_total = Sum('value')),
            many = True
            ).data


    class Meta:
        model = DeathStatistic
        fields = (
            'year',
            'year_total_value',
            'regions'
        )


class DeathStatisticBarChartSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source='group__name')
    value_total = serializers.FloatField()
    class Meta:
        model = DeathStatistic
        fields = (
            'group',
            'value_total',
        )


class DeathBarChartSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    region_value_total = serializers.FloatField()
    diseases = serializers.SerializerMethodField()

    def get_diseases(self, obj):

        return DeathStatisticBarChartSerializer(
            self.context['queryset'].filter(
                region__name = obj['region__name'],
            ).values('group__name') \
            .order_by('group__name') \
            .annotate(value_total = Sum('value')),
            many = True
            ).data


    class Meta:
        model = DeathStatistic
        fields = (
            'region',
            'region_value_total',
            'diseases'
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
    region = serializers.CharField(source='region__name')
    preventive_total = serializers.FloatField()
    curable_total = serializers.FloatField()
    preventable_total = serializers.FloatField()
    class Meta:
        model = PreventStatistic
        fields = (
            'region',
            'preventive_total',
            'curable_total',
            'preventable_total',
        )


class PreventLineChartSerializer(serializers.ModelSerializer):
    year = serializers.CharField()
    year_preventive_total = serializers.FloatField()
    year_curable_total = serializers.FloatField()
    year_preventable_total = serializers.FloatField()
    regions = serializers.SerializerMethodField()

    def get_regions(self, obj):

        return PreventStatisticLineChartSerializer(
            self.context['queryset'].filter(
                year = obj['year'],
            ).values('region__name') \
            .order_by('region__name') \
            .annotate(preventive_total = Sum('preventive')) \
            .annotate(curable_total = Sum('curable')) \
            .annotate(preventable_total = Sum('preventable')),
            many = True
            ).data


    class Meta:
        model = PreventStatistic
        fields = (
            'year',
            'year_preventive_total',
            'year_curable_total',
            'year_preventable_total',
            'regions'
        )


