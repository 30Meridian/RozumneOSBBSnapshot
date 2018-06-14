# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0007_auto_20161102_1905'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumhouse',
            name='residential_count',
            field=models.IntegerField(blank=True, null=True, verbose_name='house residential count '),
        ),
    ]
