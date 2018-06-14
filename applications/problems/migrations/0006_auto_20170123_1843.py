# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0005_auto_20161111_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='public',
            field=models.BooleanField(verbose_name='Public', help_text='Allows to view problem for users from other condominiums', default=True),
        ),
        migrations.AlterField(
            model_name='statuses',
            name='status',
            field=models.CharField(verbose_name='status', max_length=64, choices=[('waiting_board_decision', 'waiting_board_decision'), ('waiting_general_meeting', 'waiting_general_meeting'), ('inwork', 'inwork'), ('reject', 'reject'), ('done', 'done'), ('pedding', 'pedding')]),
        ),
    ]
