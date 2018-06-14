# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_conversation', '0005_auto_20160607_0455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='status',
            field=models.PositiveIntegerField(db_index=True, choices=[(0, 'Topic unlocked'), (1, 'Topic locked')], verbose_name='Topic status'),
        ),
    ]
