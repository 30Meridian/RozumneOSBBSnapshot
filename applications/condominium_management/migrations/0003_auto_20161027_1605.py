# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_city'),
        ('condominium_management', '0002_delete_proxycondominium'),
    ]

    operations = [
        migrations.CreateModel(
            name='ManagementPages',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('slug', models.CharField(max_length=32, verbose_name='Pages slug')),
                ('title', models.CharField(max_length=128, verbose_name='Pages title')),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Pages content')),
                ('condominium', models.ForeignKey(to='system.Condominium', db_column='condominium', verbose_name='Pages condominium')),
            ],
            options={
                'verbose_name_plural': 'Pages',
                'verbose_name': 'Page',
            },
        ),
        migrations.AlterUniqueTogether(
            name='managementpages',
            unique_together=set([('condominium', 'slug')]),
        ),
    ]
