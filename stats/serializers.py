from rest_framework import serializers
from django.db.models import Max, Min, Sum
from .models import (
    DiseaseGroup,
    Disease,
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


class DiseaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disease
        fields = (
            'id',
            'name',
        )


class DiseaseGroupSerializer(serializers.ModelSerializer):
    diseases = DiseaseSerializer(many = True)
    class Meta:
        model = DiseaseGroup
        fields = (
            'id',
            'name',
            'diseases'
        )


class DeathStatisticSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    disease = DiseaseSerializer()
    class Meta:
        model = DeathStatistic
        fields = (
            'region',
            'disease',
            'year',
            'age',
            'gender',
            'value',
        )


class DeathLineDataSerializer(serializers.ModelSerializer): 
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

        return DeathLineDataSerializer(
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


class DeathGroupBarDataSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source = 'disease__group__name')
    value_total = serializers.FloatField()
    class Meta:
        model = DeathStatistic
        fields = (
            'group',
            'value_total',
        )


class DeathGroupBarChartSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    region_value_total = serializers.FloatField()
    diseases = serializers.SerializerMethodField()

    def get_diseases(self, obj):

        return DeathGroupBarDataSerializer(
            self.context['queryset'].filter(
                region__name = obj['region__name'],
            ).values('disease__group__name') \
            .order_by('disease__group__name') \
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


class DeathDiseaseBarDataSerializer(serializers.ModelSerializer):
    group = serializers.CharField(source = 'disease__name')
    value_total = serializers.FloatField()
    class Meta:
        model = DeathStatistic
        fields = (
            'group',
            'value_total',
        )


class DeathDiseaseBarChartSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    region_value_total = serializers.FloatField()
    diseases = serializers.SerializerMethodField()

    def get_diseases(self, obj):

        return DeathDiseaseBarDataSerializer(
            self.context['queryset'].filter(
                region__name = obj['region__name'],
            ).values('disease__name') \
            .order_by('disease__name') \
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
    disease = serializers.CharField(source="disease.name")
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


class PreventDiseaseBarDataSerializer(serializers.ModelSerializer):
    preventive_total = serializers.FloatField()
    curable_total = serializers.FloatField()
    preventable_total = serializers.FloatField()
    disease = serializers.CharField(source="disease__name")
    class Meta:
        model = PreventStatistic
        fields = (
            'disease',
            'preventive_total',
            'curable_total',
            'preventable_total',
        )


class PreventDiseaseBarChartSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    disease_preventive_total = serializers.FloatField()
    disease_curable_total = serializers.FloatField()
    disease_preventable_total = serializers.FloatField()
    diseases = serializers.SerializerMethodField()

    def get_diseases(self, obj):

        return PreventDiseaseBarDataSerializer(
            self.context['queryset'].filter(
                region__name = obj['region__name'],
            ).values('disease__name') \
            .order_by('disease__name') \
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


class PreventGroupBarDataSerializer(serializers.ModelSerializer):
    preventive_total = serializers.FloatField()
    curable_total = serializers.FloatField()
    preventable_total = serializers.FloatField()
    disease = serializers.CharField(source="disease__group__name")
    class Meta:
        model = PreventStatistic
        fields = (
            'disease',
            'preventive_total',
            'curable_total',
            'preventable_total',
        )


class PreventGroupBarChartSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    disease_preventive_total = serializers.FloatField()
    disease_curable_total = serializers.FloatField()
    disease_preventable_total = serializers.FloatField()
    diseases = serializers.SerializerMethodField()

    def get_diseases(self, obj):

        return PreventGroupBarDataSerializer(
            self.context['queryset'].filter(
                region__name = obj['region__name'],
            ).values('disease__group__name') \
            .order_by('disease__group__name') \
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


class PreventLineDataSerializer(serializers.ModelSerializer): 
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

        return PreventLineDataSerializer(
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




