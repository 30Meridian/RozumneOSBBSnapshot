# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ideas', '0002_remove_ideas_claim'),
    ]

    operations = [
        migrations.AddField(
            model_name='ideas',
            name='public',
            field=models.BooleanField(default=True, help_text='Allows to view idea for users from other condominiums', verbose_name='Public'),
        ),
    ]
