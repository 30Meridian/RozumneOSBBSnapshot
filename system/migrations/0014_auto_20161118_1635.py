# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0013_auto_20161118_1332'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='address',
        ),
        migrations.AddField(
            model_name='condominiumnonresidentialpremise',
            name='user',
            field=models.ForeignKey(db_column='user', verbose_name='non residential owner', to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='condominiumresidentialpremise',
            name='user',
            field=models.ForeignKey(db_column='user', verbose_name='residential owner', to=settings.AUTH_USER_MODEL, default=1),
            preserve_default=False,
        ),
    ]
