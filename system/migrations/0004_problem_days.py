# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_alter_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumhouse',
            name='object_registry',
            field=models.ForeignKey(null=True, verbose_name='object_registry', to='system.ObjectRegistry'),
        ),
        migrations.AlterField(
            model_name='user',
            name='owned',
            field=models.ManyToManyField(to='system.ObjectRegistry', verbose_name='owned'),
        ),
    ]
