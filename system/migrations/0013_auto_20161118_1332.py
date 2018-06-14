# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0012_auto_20161114_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumfloor',
            name='name',
            field=models.CharField(max_length=32, blank=True, verbose_name='floor name'),
        ),
        migrations.AlterField(
            model_name='condominiumporch',
            name='name',
            field=models.CharField(max_length=64, default='', blank=True, verbose_name='porch name'),
            preserve_default=False,
        ),
    ]
