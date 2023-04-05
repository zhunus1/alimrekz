import datetime
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

def current_year():
        return datetime.date.today().year
    
def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)

# Create your models here.
class StatisticDocument(models.Model):
    
    document = models.FileField(upload_to='files/')
    year = models.CharField(
        max_length = 255,
    )

    def __str__(self):
        return self.year


class DiseaseGroup(models.Model):
    name = models.CharField(
        max_length = 255,
    )
    
    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(
        max_length = 255,
    )
    def __str__(self):
        return self.name


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
        on_delete = models.CASCADE
    )
    group = models.ForeignKey(
        DiseaseGroup, 
        on_delete = models.CASCADE
    )
    year = models.PositiveIntegerField(
        validators = [
            MinValueValidator(2015), 
            max_value_current_year
        ]
    )
    age = models.CharField(
        max_length = 5, 
        choices = AGES,
    )
    gender = models.CharField(
        max_length = 5, 
        choices = GENDERS,
    )
    value = models.FloatField()
    disease_name = models.CharField(
        max_length = 255,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields = [
                    'region', 
                    'year',
                    'age',
                    'gender',
                    'disease_name'
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
        on_delete = models.CASCADE
    )

    year = models.PositiveIntegerField(
        validators = [
            MinValueValidator(2015), 
            max_value_current_year
        ]
    )

    disease = models.CharField(
        max_length = 255,
    )

    standard = models.CharField(
        max_length = 5, 
        choices = STANDARDS,
    )

    gender = models.CharField(
        max_length = 5, 
        choices = GENDERS,
    )

    preventive =  models.FloatField()

    curable = models.FloatField()

    preventable = models.FloatField()

    class Meta:
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