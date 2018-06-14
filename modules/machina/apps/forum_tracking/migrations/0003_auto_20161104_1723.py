# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_tracking', '0002_auto_20160607_0502'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forumreadtrack',
            name='mark_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Mark time', db_index=True),
        ),
        migrations.AlterField(
            model_name='topicreadtrack',
            name='mark_time',
            field=models.DateTimeField(auto_now=True, verbose_name='Mark time', db_index=True),
        ),
    ]
