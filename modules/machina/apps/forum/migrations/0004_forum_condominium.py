# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
        ('forum', '0003_remove_forum_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='condominium',
            field=models.ForeignKey(blank=True, to='system.Condominium', null=True),
        ),
    ]
