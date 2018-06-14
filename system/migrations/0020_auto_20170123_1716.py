# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('condominium_management', '0006_delete_proxycondominium'),
        ('system', '0019_auto_20170113_1545'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyManagementPages',
            fields=[
            ],
            options={
                'verbose_name_plural': 'Pages',
                'verbose_name': 'Page',
                'proxy': True,
            },
            bases=('condominium_management.managementpages',),
        ),

        migrations.AddField(
            model_name='condominium',
            name='public_ideas',
            field=models.BooleanField(verbose_name='Public ideas', default=True, help_text='Allows by default to view ideas for users from other condominiums '),
        ),
        migrations.AddField(
            model_name='condominium',
            name='public_news',
            field=models.BooleanField(verbose_name='Public news', default=True, help_text='Allows by default to view news for users from other condominiums '),
        ),
        migrations.AddField(
            model_name='condominium',
            name='public_polls',
            field=models.BooleanField(verbose_name='Public polls', default=True, help_text='Allows by default to view polls for users from other condominiums '),
        ),
        migrations.AddField(
            model_name='condominium',
            name='public_problems',
            field=models.BooleanField(verbose_name='Public problems', default=True, help_text='Allows by default to view problems for users from other condominiums '),
        ),
        migrations.AlterField(
            model_name='condominium',
            name='datetime_created',
            field=models.DateTimeField(verbose_name='Registration date', auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='area',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0.01)], verbose_name='house area '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='description',
            field=models.CharField(blank=True, verbose_name='house description ', max_length=255),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='elevators_count',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='house elevators count '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='entrance_count',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='house entrance count '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='max_floors',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='house max floors '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='min_floors',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='house min floors '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='name',
            field=models.CharField(blank=True, verbose_name='house name ', max_length=64),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='residential_area',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='house residential area '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='residential_count',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='house residential count '),
        ),
        migrations.AlterField(
            model_name='condominiumnonresidentialpremise',
            name='house',
            field=models.ForeignKey(to='system.CondominiumHouse', db_column='house', verbose_name='non residental house'),
        ),
        migrations.AlterField(
            model_name='condominiumnonresidentialpremise',
            name='number',
            field=models.CharField(blank=True, verbose_name='non residential number or name', max_length=32),
        ),
        migrations.AlterField(
            model_name='condominiumposition',
            name='position',
            field=models.CharField(verbose_name='position', max_length=16, choices=[('chairman', 'Сhairman'), ('vice-chairman', 'Vice-Chairman'), ('secretary', 'Secretary'), ('trustee', 'Trustee'), ('audit-member', 'Audit team member'), ('member', 'Member'), ('inhabitant', 'Inhabitant')]),
        ),
        migrations.AlterField(
            model_name='condominiumresidentialpremise',
            name='number',
            field=models.CharField(blank=True, verbose_name='residential number or name', max_length=32),
        ),
    ]
