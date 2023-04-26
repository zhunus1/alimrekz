from django.contrib import admin
from .models import (
    StatisticDocument,
    DiseaseGroup,
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
        'year',
    )

@admin.register(DiseaseGroup)
class DiseaseGroupModelAdmin(admin.ModelAdmin):
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
        'group',
        'year',
        'age',
        'gender',
        'value',
        'disease_name',
    )

@admin.register(PreventStatistic)
class PreventStatisticModelAdmin(admin.ModelAdmin):
    fields = (
        'region',
        'year',
        'group',
        'disease',
        'standard',
        'gender',
        'preventive',
        'curable',
        'preventable'
    )