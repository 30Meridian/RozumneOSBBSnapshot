# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pages',
            name='datetime_update',
            field=models.DateTimeField(verbose_name='Pages datetime', default=datetime.datetime(2016, 11, 21, 15, 26, 53, 242799), auto_now=True),
            preserve_default=False,
        ),
    ]
