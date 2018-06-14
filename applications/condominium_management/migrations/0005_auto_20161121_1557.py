# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import datetime


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('condominium_management', '0004_proxycondominium'),
    ]

    operations = [
        migrations.AddField(
            model_name='managementpages',
            name='author',
            field=models.ForeignKey(db_column='author', to=settings.AUTH_USER_MODEL, null=True, blank=True, verbose_name='Pages author'),
        ),
        migrations.AddField(
            model_name='managementpages',
            name='datetime',
            field=models.DateTimeField(default=datetime.datetime(2016, 11, 21, 15, 57, 20, 338542), auto_now_add=True, verbose_name='Datetime'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='managementpages',
            name='datetime_update',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2016, 11, 21, 15, 57, 35, 638975), verbose_name='Datetime update'),
            preserve_default=False,
        ),
    ]
