# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyCondominium',
            fields=[
            ],
            options={
                'verbose_name': 'Condominium modules',
                'verbose_name_plural': 'Condominium modules',
                'proxy': True,
            },
            bases=('system.condominium',),
        ),
    ]
