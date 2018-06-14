# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0017_condominium_problem_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominiumnonresidentialpremise',
            name='house',
            field=models.ForeignKey(verbose_name='residental house', default=1, to='system.CondominiumHouse', db_column='house'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='condominiumresidentialpremise',
            name='house',
            field=models.ForeignKey(verbose_name='residental house', default=1, to='system.CondominiumHouse', db_column='house'),
            preserve_default=False,
        ),
    ]
