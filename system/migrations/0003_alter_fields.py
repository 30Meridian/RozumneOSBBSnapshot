# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_auto_20161031_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominium',
            name='name',
            field=models.CharField(blank=True, max_length=64, verbose_name='name condominium'),
        ),
        migrations.AlterField(
            model_name='objecttypes',
            name='category',
            field=models.CharField(max_length=64),
        ),
    ]
