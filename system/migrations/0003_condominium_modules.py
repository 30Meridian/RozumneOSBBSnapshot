# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0002_modules_parent'),
    ]

    operations = [
        migrations.CreateModel(
            name='CondominiumModules',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('condominium', models.ForeignKey(to='system.Condominium')),
                ('module', models.ForeignKey(to='system.Modules')),
                ('use', models.BooleanField()),
                ('weight', models.IntegerField()),
            ],
            options={
                'verbose_name': 'condominium module',
                'verbose_name_plural': 'condominium modules',
                'db_table': 'condominium_modules',
            },
        ),
        migrations.AlterField(
            model_name='condominiumconnectedutility',
            name='object_registry',
            field=models.ForeignKey(verbose_name='object registry', to='system.ObjectRegistry', db_column='object_registry'),
        ),
        migrations.AlterField(
            model_name='condominiumconnectedutility',
            name='service',
            field=models.ForeignKey(verbose_name='service', to='system.EngineeringService', db_column='service'),
        ),
        migrations.AlterField(
            model_name='condominiumconnectedutility',
            name='start_value',
            field=models.FloatField(verbose_name='start value'),
        ),
    ]
