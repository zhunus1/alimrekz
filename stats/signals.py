import pandas as pd
from django.db.models.signals import post_save
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
        document = instance.document.path
        xls = pd.ExcelFile(document)
        pages = xls.sheet_names
        death = pd.read_excel(xls, sheet_name = pages[0])
        prevent = pd.read_excel(xls, sheet_name = pages[1])

        columns = list(death.columns.values)
        diseases = columns[columns.index('пол') + 1:]

        death_records = []

        for index, row in death.iterrows():

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
                death_records.append(
                    DeathStatistic(
                        year = year,
                        region = region,
                        disease_name = disease,
                        age = age,
                        gender = gender,
                        group = group,
                        value = row[disease],
                    )
                )

        death_objects = DeathStatistic.objects.bulk_create(
            death_records, 
            batch_size = 250, 
            ignore_conflicts = True
        )

        prevent_records = []

        for index, row in prevent.iterrows():
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

        #TO-DO: Write the code to separate each years file in each folder