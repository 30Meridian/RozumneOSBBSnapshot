# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='public',
            field=models.BooleanField(verbose_name='Public', default=True, help_text='Allows to view article for users from other condominiums'),
        ),
    ]
