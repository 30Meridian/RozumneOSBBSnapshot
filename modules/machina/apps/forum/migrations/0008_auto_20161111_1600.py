# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0007_proxyforumconversationattachment_proxyforumconversationpost_proxyforumconversationtopic_proxyforumco'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='condominium',
            field=models.ForeignKey(null=True, blank=True, verbose_name='Condominium', to='system.Condominium'),
        ),
    ]
