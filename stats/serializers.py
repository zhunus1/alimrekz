from rest_framework import serializers
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
            'id',
            'region',
            'group',
            'year',
            'age',
            'gender',
            'disease_name',
            'value',
        )


class PreventStatisticSerializer(serializers.ModelSerializer):
    region = RegionSerializer()
    class Meta:
        model = PreventStatistic
        fields = (
            'id',
            'year',
            'disease',
            'region',
            'standard',
            'gender',
            'preventive',
            'curable',
            'preventable',
        )