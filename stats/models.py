import os
import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator, FileExtensionValidator


def current_year():
    return datetime.date.today().year
    
def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

# Create your models here.
class StatisticDocument(models.Model):
    TYPES = (
        ('rude', 'Грубая смертность'),
        ('prevent', 'Предотвратимая смертность'),
    )

    document_type = models.CharField(
        max_length = 25, 
        choices = TYPES,
        verbose_name = "Тип документа",
    )

    document = models.FileField(
        upload_to = 'documents/',
        validators = [
            FileExtensionValidator(
                allowed_extensions=["csv"]
            )
        ],
        verbose_name = "Документ",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )

    def __str__(self):
        return str(self.pk)
    
    class Meta:
        verbose_name = "Документ"
        verbose_name_plural = "Документы"


class DiseaseGroup(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = "Название",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Группа заболеваний"
        verbose_name_plural = "Группы заболеваний"


class Disease(models.Model):
    group = models.ForeignKey(
        DiseaseGroup, 
        on_delete = models.CASCADE,
        verbose_name = "Группа заболевания",
        related_name = 'diseases'
    )
    
    name = models.CharField(
        max_length = 255,
        verbose_name = "Название",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Заболевание"
        verbose_name_plural = "Заболевания"


class Region(models.Model):
    name = models.CharField(
        max_length = 255,
        verbose_name = "Название",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Регион"
        verbose_name_plural = "Регионы"


class DeathStatistic(models.Model):
    GENDERS = (
        ('муж', 'муж'),
        ('жен', 'жен'),
        ('всего', 'всего'),
    )

    AGES = (
        ('0-4', '0-4'),
        ('5-9', '5-9'),
        ('10-14', '10-14'),
        ('15-19', '15-19'),
        ('20-24', '20-24'),
        ('25-29', '25-29'),
        ('30-34', '30-34'),
        ('35-39', '35-39'),
        ('40-44', '40-44'),
        ('45-49', '45-49'),
        ('50-54', '50-54'),
        ('55-59', '55-59'),
        ('60-64', '60-64'),
        ('65-69', '65-69'),
        ('70-74', '70-74'),
    )

    region = models.ForeignKey(
        Region, 
        on_delete = models.CASCADE,
        verbose_name = "Регион",
    )

    disease = models.ForeignKey(
        Disease, 
        on_delete = models.CASCADE,
        verbose_name = "Заболевание",
    )

    year = models.PositiveIntegerField(
        validators = [
            MinValueValidator(1991), 
            max_value_current_year
        ],
        verbose_name = "Год",
    )

    age = models.CharField(
        max_length = 5, 
        choices = AGES,
        verbose_name = "Возраст",
    )

    gender = models.CharField(
        max_length = 5, 
        choices = GENDERS,
        verbose_name = "Пол",
    )

    value = models.FloatField(
        verbose_name = "Значение",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )

    class Meta:
        verbose_name = "Грубая смертность"
        verbose_name_plural = "Грубая смертность"
        constraints = [
            models.UniqueConstraint(
                fields = [
                    'region', 
                    'year',
                    'age',
                    'gender',
                    'disease'
                ],
                name = "death_statistic_unique"
            )
        ]


class PreventStatistic(models.Model):
    GENDERS = (
        ('муж', 'муж'),
        ('жен', 'жен'),
        ('всего', 'всего'),
    )

    STANDARDS = (
        ('ОЭСР', 'ОЭСР'),
        ('по РК', 'по РК'),
    )

    region = models.ForeignKey(
        Region, 
        on_delete = models.CASCADE,
        verbose_name = "Регион",
    )

    year = models.PositiveIntegerField(
        validators = [
            MinValueValidator(1991), 
            max_value_current_year
        ],
        verbose_name = "Год",
    )

    disease = models.ForeignKey(
        Disease, 
        on_delete = models.CASCADE,
        verbose_name = "Заболевание",
    )

    standard = models.CharField(
        max_length = 5, 
        choices = STANDARDS,
        verbose_name = "Стандарт",
    )

    gender = models.CharField(
        max_length = 5, 
        choices = GENDERS,
        verbose_name = "Пол",
    )

    preventive =  models.FloatField(
        verbose_name = "Превентивный",
    )

    curable = models.FloatField(
        verbose_name = "Излечимый",
    )

    preventable = models.FloatField(
        verbose_name = "Предотвратимый",
    )

    created = models.DateTimeField(
        verbose_name = "Создано",
        auto_now_add = True,
    )

    updated = models.DateTimeField(
        verbose_name = "Обновлено",
        auto_now = True,
    )

    class Meta:
        verbose_name = "Предотвратимая смертность"
        verbose_name_plural = "Предотвратимая смертность"
        constraints = [
            models.UniqueConstraint(
                fields = [
                    'region', 
                    'year',
                    'disease',
                    'standard',
                    'gender'
                ],
                name = "prevent_statistic_unique"
            )
        ]  