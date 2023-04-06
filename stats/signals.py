import os
import pandas as pd
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .common import *
from .models import (
    StatisticDocument,
    DiseaseGroup,
    Region,
    DeathStatistic,
    PreventStatistic
)

def find_group(val, dictionary):
    for k, v in dictionary.items():
        if val in v:
            return k
 
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
                    group_name = find_group(disease, disease_groups)
                    group = DiseaseGroup.objects.get(
                        name = group_name,
                    )
                    value = row[disease]

                    death_records.append(
                        DeathStatistic(
                            year = year,
                            region = region,
                            disease_name = disease,
                            age = age,
                            gender = gender,
                            group = group,
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
                prevent_records.append(
                    PreventStatistic(
                        region = region,
                        year = row['годы'],
                        disease = row['Тип заболевания'],
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