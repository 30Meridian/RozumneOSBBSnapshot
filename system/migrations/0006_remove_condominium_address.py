# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0005_condomonium_registration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='condominium',
            name='address',
        ),
    ]
