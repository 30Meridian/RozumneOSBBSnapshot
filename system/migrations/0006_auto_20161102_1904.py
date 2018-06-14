# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_auto_20161102_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumhouse',
            name='elevators_count',
            field=models.IntegerField(verbose_name='house elevators count ', blank=True),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='entrance_count',
            field=models.IntegerField(verbose_name='house entrance count ', blank=True),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='max_floors',
            field=models.IntegerField(verbose_name='house max floors ', blank=True),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='min_floors',
            field=models.IntegerField(verbose_name='house min floors ', blank=True),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='residential_count',
            field=models.IntegerField(verbose_name='house residential count ', blank=True),
        ),
    ]
