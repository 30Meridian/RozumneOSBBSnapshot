# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0010_condominium_problem_days'),
        ('condominium_management', '0003_auto_20161027_1605'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyCondominium',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name': 'Condominium modules',
                'verbose_name_plural': 'Condominium modules',
            },
            bases=('system.condominium',),
        ),
    ]
