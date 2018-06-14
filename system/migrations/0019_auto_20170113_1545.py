# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.core.validators
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0018_auto_20161122_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominium',
            name='datetime_created',
            field=models.DateTimeField(default=datetime.datetime(2017, 1, 13, 15, 44, 43, 209502), auto_now_add=True),
            preserve_default=False,
        ),

    ]
