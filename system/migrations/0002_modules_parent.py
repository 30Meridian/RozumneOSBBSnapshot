# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modules',
            name='parent',
            field=models.ForeignKey(to='system.Modules', null=True),
        ),
    ]
