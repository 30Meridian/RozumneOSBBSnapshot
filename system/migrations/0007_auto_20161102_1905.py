# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_auto_20161102_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumhouse',
            name='elevators_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='house elevators count '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='entrance_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='house entrance count '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='max_floors',
            field=models.IntegerField(blank=True, null=True, verbose_name='house max floors '),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='min_floors',
            field=models.IntegerField(blank=True, null=True, verbose_name='house min floors '),
        ),
    ]
