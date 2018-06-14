# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_problem_days'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condominiumcommonarea',
            name='object_registry',
            field=models.ForeignKey(verbose_name='object_registry', to='system.ObjectRegistry', db_column='object_registry'),
        ),
        migrations.AlterField(
            model_name='condominiumfloor',
            name='object_registry',
            field=models.ForeignKey(verbose_name='object_registry', null=True, to='system.ObjectRegistry'),
        ),
        migrations.AddField(
            model_name='condominiumhouse',
            name='address',
            field=models.CharField(verbose_name='house address ', max_length=128, db_column='address'),
        ),
        migrations.AlterField(
            model_name='condominiuminfrastructure',
            name='object_registry',
            field=models.ForeignKey(verbose_name='object_registry', to='system.ObjectRegistry', db_column='object_registry'),
        ),
        migrations.AlterField(
            model_name='condominiummodules',
            name='condominium',
            field=models.ForeignKey(verbose_name='condominium', to='system.Condominium'),
        ),
        migrations.AlterField(
            model_name='condominiummodules',
            name='module',
            field=models.ForeignKey(verbose_name='module', to='system.Modules'),
        ),
        migrations.AlterField(
            model_name='condominiummodules',
            name='use',
            field=models.BooleanField(verbose_name='use'),
        ),
        migrations.AlterField(
            model_name='condominiummodules',
            name='weight',
            field=models.IntegerField(verbose_name='weight'),
        ),
        migrations.AlterField(
            model_name='condominiumnonresidentialpremise',
            name='object_registry',
            field=models.ForeignKey(verbose_name='object_registry', null=True, to='system.ObjectRegistry'),
        ),
        migrations.AlterField(
            model_name='condominiumporch',
            name='object_registry',
            field=models.ForeignKey(verbose_name='object_registry', null=True, to='system.ObjectRegistry'),
        ),
        migrations.AlterField(
            model_name='condominiumresidentialpremise',
            name='object_registry',
            field=models.ForeignKey(verbose_name='object_registry', null=True, to='system.ObjectRegistry'),
        ),
        migrations.DeleteModel(
            name='Address',
        ),
    ]
