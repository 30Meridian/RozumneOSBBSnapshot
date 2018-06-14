# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0006_remove_condominium_address'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominium',
            name='legal_address',
            field=models.CharField(max_length=128, verbose_name='legal address', default=' '),
            preserve_default=False,
        ),
    ]
