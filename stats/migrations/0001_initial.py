# Generated by Django 3.2.18 on 2023-05-01 04:12

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import stats.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Disease',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Заболевание',
                'verbose_name_plural': 'Заболевания',
            },
        ),
        migrations.CreateModel(
            name='DiseaseGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Группа болезни',
                'verbose_name_plural': 'Группа болезней',
            },
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Регион',
                'verbose_name_plural': 'Регионы',
            },
        ),
        migrations.CreateModel(
            name='StatisticDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document_type', models.CharField(choices=[('rude', 'Грубая смертность'), ('prevent', 'Предотвратимая смертность')], max_length=25, verbose_name='Тип документа')),
                ('document', models.FileField(upload_to='documents/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['csv'])], verbose_name='Документ')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
            ],
            options={
                'verbose_name': 'Документ',
                'verbose_name_plural': 'Документы',
            },
        ),
        migrations.CreateModel(
            name='PreventStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1991), stats.models.max_value_current_year], verbose_name='Год')),
                ('standard', models.CharField(choices=[('ОЭСР', 'ОЭСР'), ('по РК', 'по РК')], max_length=5, verbose_name='Стандарт')),
                ('gender', models.CharField(choices=[('муж', 'муж'), ('жен', 'жен'), ('всего', 'всего')], max_length=5, verbose_name='Пол')),
                ('preventive', models.FloatField(verbose_name='Превентивный')),
                ('curable', models.FloatField(verbose_name='Излечимый')),
                ('preventable', models.FloatField(verbose_name='Предотвратимый')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.disease', verbose_name='Заболевание')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Предотвратимая смертность',
                'verbose_name_plural': 'Предотвратимая смертность',
            },
        ),
        migrations.AddField(
            model_name='disease',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.diseasegroup', verbose_name='Группа заболевания'),
        ),
        migrations.CreateModel(
            name='DeathStatistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1991), stats.models.max_value_current_year], verbose_name='Год')),
                ('age', models.CharField(choices=[('0-4', '0-4'), ('5-9', '5-9'), ('10-14', '10-14'), ('15-19', '15-19'), ('20-24', '20-24'), ('25-29', '25-29'), ('30-34', '30-34'), ('35-39', '35-39'), ('40-44', '40-44'), ('45-49', '45-49'), ('50-54', '50-54'), ('55-59', '55-59'), ('60-64', '60-64'), ('65-69', '65-69'), ('70-74', '70-74')], max_length=5, verbose_name='Возраст')),
                ('gender', models.CharField(choices=[('муж', 'муж'), ('жен', 'жен'), ('всего', 'всего')], max_length=5, verbose_name='Пол')),
                ('value', models.FloatField(verbose_name='Значение')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Создано')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Обновлено')),
                ('disease', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.disease', verbose_name='Заболевание')),
                ('region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='stats.region', verbose_name='Регион')),
            ],
            options={
                'verbose_name': 'Грубая смертность',
                'verbose_name_plural': 'Грубая смертность',
            },
        ),
        migrations.AddConstraint(
            model_name='preventstatistic',
            constraint=models.UniqueConstraint(fields=('region', 'year', 'disease', 'standard', 'gender'), name='prevent_statistic_unique'),
        ),
        migrations.AddConstraint(
            model_name='deathstatistic',
            constraint=models.UniqueConstraint(fields=('region', 'year', 'age', 'gender', 'disease'), name='death_statistic_unique'),
        ),
    ]
