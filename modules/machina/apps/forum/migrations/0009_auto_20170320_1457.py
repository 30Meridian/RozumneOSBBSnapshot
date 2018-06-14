# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0008_auto_20161111_1600'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='type',
            field=models.PositiveSmallIntegerField(db_index=True, choices=[(0, 'Default forum'), (1, 'Category forum')], verbose_name='Forum type'),
        ),
    ]
