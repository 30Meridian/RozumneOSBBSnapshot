# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0006_auto_20170123_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuses',
            name='status',
            field=models.CharField(verbose_name='status', max_length=64, choices=[('reject', 'reject'), ('inwork', 'inwork'), ('waiting_general_meeting', 'waiting_general_meeting'), ('waiting_board_decision', 'waiting_board_decision'), ('pedding', 'pedding'), ('done', 'done')]),
        ),
    ]
