import os
import pandas as pd
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import (
    StatisticDocument,
    DiseaseGroup,
    Disease,
    Region,
    DeathStatistic,
    PreventStatistic
)
 
@receiver(post_save, sender = StatisticDocument)
def create_data(sender, instance, created, **kwargs):

    if created:
        path = instance.document.path
        document = pd.read_csv(path, decimal = ',')
        choice = instance.document_type

        if choice == 'rude':
            columns = list(document.columns.values)
            diseases = columns[columns.index('пол') + 1:]

            death_records = []

            for index, row in document.iterrows():

                year = row['годы']
                region = Region.objects.get(
                    name = row['регион'],
                )
                age = row['возраст']
                gender = row['пол']


                for disease in diseases:
                    value = row[disease]
                    disease = Disease.objects.get(
                        name = disease,
                    )
                    
                    death_records.append(
                        DeathStatistic(
                            year = year,
                            region = region,
                            disease = disease,
                            age = age,
                            gender = gender,
                            value = value,
                        )
                    )

            death_objects = DeathStatistic.objects.bulk_create(
                death_records, 
                batch_size = 250, 
                ignore_conflicts = True
            )
        else:
            
            prevent_records = []

            for index, row in document.iterrows():
                region = Region.objects.get(
                    name = row['регион'],
                )
                disease = Disease.objects.get(
                    name = row['Тип заболевания'],
                )

                prevent_records.append(
                    PreventStatistic(
                        region = region,
                        year = row['годы'],
                        disease = disease,
                        standard = row['Стандарт'],
                        gender = row['Пол'],
                        preventive = row['Превентивная'],
                        curable = row['Излечимая'],
                        preventable = row['Предотвратимая']
                    )
                )
            
            prevent_objects = PreventStatistic.objects.bulk_create(
                prevent_records, 
                batch_size = 250, 
                ignore_conflicts = True
            )



@receiver(post_delete, sender = StatisticDocument)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    if instance.document:
        if os.path.isfile(instance.document.path):
            os.remove(instance.document.path)