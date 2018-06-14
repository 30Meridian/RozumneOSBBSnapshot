# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_auto_20161111_1600'),
        ('auth', '0006_require_contenttypes_0002'),
        ('account', '0002_auto_20161017_1550'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyGroup',
            fields=[
            ],
            options={
                'verbose_name': 'Group',
                'verbose_name_plural': 'Groups',
                'proxy': True,
            },
            bases=('auth.group',),
            managers=[
                ('objects', django.contrib.auth.models.GroupManager()),
            ],
        ),
        migrations.CreateModel(
            name='ProxyUser',
            fields=[
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
                'proxy': True,
            },
            bases=('system.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
