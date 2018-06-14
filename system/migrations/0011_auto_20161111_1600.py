# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_condominium_problem_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumcommonarea',
            name='description',
            field=models.CharField(max_length=255, verbose_name='common area description'),
        ),
        migrations.AlterField(
            model_name='condominiuminfrastructure',
            name='description',
            field=models.CharField(max_length=255, verbose_name='infrastructure description'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(max_length=64, verbose_name='user phone'),
        ),
    ]
