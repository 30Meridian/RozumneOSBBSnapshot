# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0004_auto_20161104_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuses',
            name='resolution',
            field=models.CharField(blank=True, max_length=3000, verbose_name='resolution'),
        ),
        migrations.AlterField(
            model_name='statuses',
            name='status',
            field=models.CharField(max_length=64, choices=[('inwork', 'inwork'), ('pedding', 'pedding'), ('reject', 'reject'), ('done', 'done'), ('waiting_general_meeting', 'waiting_general_meeting'), ('waiting_board_decision', 'waiting_board_decision')], verbose_name='status'),
        ),
    ]
