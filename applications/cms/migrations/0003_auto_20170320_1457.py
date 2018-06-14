# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0002_pages_datetime_update'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pages',
            name='datetime_update',
            field=models.DateTimeField(auto_now=True, verbose_name='Pages datetime update'),
        ),
    ]
