# Generated by Django 3.2.18 on 2023-04-05 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0001_initial'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='deathstatistic',
            constraint=models.UniqueConstraint(fields=('region', 'year', 'age', 'gender', 'disease_name'), name='unique'),
        ),
    ]
