# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0003_auto_20161101_1743'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuses',
            name='status',
            field=models.CharField(choices=[('waiting_general_meeting', 'waiting_general_meeting'), ('inwork', 'inwork'), ('reject', 'reject'), ('pedding', 'pedding'), ('done', 'done'), ('waiting_board_decision', 'waiting_board_decision')], verbose_name='status', max_length=64),
        ),
    ]
