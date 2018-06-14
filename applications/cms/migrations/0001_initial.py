# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ckeditor_uploader.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pages',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('datetime', models.DateTimeField(verbose_name='Pages datetime', auto_now_add=True)),
                ('slug', models.CharField(verbose_name='Pages slug', max_length=32)),
                ('title', models.CharField(verbose_name='Pages title', max_length=128)),
                ('content', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='Pages content')),
                ('author', models.ForeignKey(db_column='author', verbose_name='Pages author', to=settings.AUTH_USER_MODEL)),
                ('condominium', models.ForeignKey(db_column='condominium', verbose_name='Pages condominium', to='system.Condominium')),
            ],
            options={
                'verbose_name': 'Page',
                'verbose_name_plural': 'Pages',
            },
        ),
        migrations.AlterUniqueTogether(
            name='pages',
            unique_together=set([('condominium', 'slug')]),
        ),
    ]
