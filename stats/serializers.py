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
    class Meta:
        model = PreventStatistic
        fields = (
            'disease',
            'preventive',
            'curable',
            'preventable',
        )


class PreventListSerializer(serializers.ModelSerializer):
    region = serializers.CharField(source='region__name')
    preventive_total_value = serializers.FloatField()
    curable_total_value = serializers.FloatField()
    preventable_total_value = serializers.FloatField()
    diseases = serializers.SerializerMethodField()

    def get_diseases(self, obj):
        return PreventStatisticSerializer(
                    PreventStatistic.objects.filter( 
                        region__name = obj['region__name'],
                        year = obj['year'],
                        gender = obj['gender'],
                        standard = obj['standard']
                    ), 
                    many = True).data
                

    class Meta:
        model = PreventStatistic
        fields = (
            'region',
            'preventive_total_value',
            'curable_total_value',
            'preventable_total_value',
            'diseases'
        )
