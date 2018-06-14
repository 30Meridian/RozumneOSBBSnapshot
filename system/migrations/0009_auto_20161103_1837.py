# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0008_auto_20161102_1907'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumfloor',
            name='lighting_points',
            field=models.IntegerField(blank=True, verbose_name='floor lighting_points', null=True, default=1),
        ),
        migrations.AlterField(
            model_name='condominiumfloor',
            name='name',
            field=models.CharField(verbose_name='floor name', max_length=32),
        ),
        migrations.AlterField(
            model_name='condominiumfloor',
            name='non_residential_count',
            field=models.IntegerField(blank=True, verbose_name='floor non_residential_count', null=True, default=0),
        ),
        migrations.AlterField(
            model_name='condominiumfloor',
            name='residential_count',
            field=models.IntegerField(blank=True, verbose_name='floor residential_count', null=True),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='residential_area',
            field=models.FloatField(blank=True, verbose_name='house residential area ', null=True),
        ),
        migrations.AlterField(
            model_name='condominiumporch',
            name='elevators_count',
            field=models.IntegerField(blank=True, verbose_name='porch elevators_count', null=True),
        ),
        migrations.AlterField(
            model_name='condominiumporch',
            name='lighting_points',
            field=models.IntegerField(blank=True, verbose_name='porch lighting_points', null=True),
        ),
        migrations.AlterField(
            model_name='condominiumporch',
            name='non_residential_count',
            field=models.IntegerField(blank=True, verbose_name='porch non_residential_count', null=True, default=0),
        ),
        migrations.AlterField(
            model_name='condominiumporch',
            name='residential_count',
            field=models.IntegerField(blank=True, verbose_name='porch residential_count', null=True),
        ),
    ]
