# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_squashed_0007_condominium_legal_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominium',
            name='document',
            field=models.FileField(upload_to='documents/', verbose_name='condominium constitution'),
        ),
    ]
