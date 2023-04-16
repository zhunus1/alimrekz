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
    region = RegionSerializer()
    class Meta:
        model = PreventStatistic
        fields = (
            'year',
            'region',
            'disease',
            'preventive',
            'curable',
            'preventable',
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


class PreventListSerializer(serializers.ModelSerializer):
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
