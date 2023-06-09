from django.contrib import admin
from .models import (
    StatisticDocument,
    DiseaseGroup,
    Disease,
    Region,
    DeathStatistic,
    PreventStatistic
)

# Register your models here.
@admin.register(StatisticDocument)
class StatisticDocumentModelAdmin(admin.ModelAdmin):
    fields = (
        'document_type',
        'document',
    )

@admin.register(DiseaseGroup)
class DiseaseGroupModelAdmin(admin.ModelAdmin):
    fields = (
        'name',
    )

@admin.register(Disease)
class DiseaseModelAdmin(admin.ModelAdmin):
    fields = (
        'name',
    )

@admin.register(Region)
class RegionModelAdmin(admin.ModelAdmin):
    fields = (
        'name',
    )

@admin.register(DeathStatistic)
class DeathStatisticModelAdmin(admin.ModelAdmin):
    fields = (
        'region',
        'year',
        'age',
        'gender',
        'value',
        'disease',
    )

@admin.register(PreventStatistic)
class PreventStatisticModelAdmin(admin.ModelAdmin):
    fields = (
        'region',
        'year',
        'disease',
        'standard',
        'gender',
        'preventive',
        'curable',
        'preventable'
    )