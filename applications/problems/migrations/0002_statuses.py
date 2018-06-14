# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statuses',
            name='status',
            field=models.CharField(choices=[(2, 'inwork'), (3, 'waiting_board_decision'), (6, 'reject'), (4, 'waiting_general_meeting'), (1, 'pedding'), (5, 'done')], max_length=1),
        ),
    ]
