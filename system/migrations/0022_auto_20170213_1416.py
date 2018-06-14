# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0021_condominium_problem_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominium',
            name='latitude',
            field=models.CharField(max_length=64, blank=True),
        ),
        migrations.AddField(
            model_name='condominium',
            name='longitude',
            field=models.CharField(max_length=64, blank=True),
        ),
        # migrations.AddField(
        #     model_name='condominium',
        #     name='problem_days',
        #     field=models.IntegerField(default=7, verbose_name='problem condominium'),
        # ),
    ]
