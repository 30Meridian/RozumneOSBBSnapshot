# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import system.validators
import system.models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0011_auto_20161111_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='condominiumfloor',
            name='number',
            field=models.IntegerField(default=1, verbose_name='floor number'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='condominium',
            name='document',
            field=models.FileField(upload_to=system.models.get_document_path, verbose_name='condominium constitution', validators=[system.validators.validate_file_extension]),
        ),
        migrations.AlterField(
            model_name='condominium',
            name='name',
            field=models.CharField(max_length=64, verbose_name='name condominium'),
        ),
        migrations.AlterField(
            model_name='condominiumcommonarea',
            name='description',
            field=models.CharField(max_length=255, blank=True, verbose_name='common area description'),
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='max_floors',
            field=models.IntegerField(default=1, verbose_name='house max floors '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='condominiumhouse',
            name='min_floors',
            field=models.IntegerField(default=1, verbose_name='house min floors '),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='condominiuminfrastructure',
            name='description',
            field=models.CharField(null=True, blank=True, verbose_name='infrastructure description', max_length=255),
        ),
    ]
