# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import news.models
import stdimage.models
import ckeditor_uploader.fields


class Migration(migrations.Migration):



    operations = [
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('datetime', models.DateTimeField(verbose_name='Datetime', auto_now_add=True)),
                ('datetime_publish', models.DateTimeField(verbose_name='Datetime_publish')),
                ('title', models.CharField(verbose_name='Title', max_length=150)),
                ('shortdesc', models.CharField(verbose_name='Short description', max_length=300)),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='News text')),
                ('mainimg', stdimage.models.StdImageField(verbose_name='Main img', upload_to=news.models.get_file_path)),
                ('publish', models.BooleanField(verbose_name='Publish')),
                ('author', models.ForeignKey(db_column='author', to=settings.AUTH_USER_MODEL, verbose_name='Author')),
                ('condominium', models.ForeignKey(db_column='condominium', to='system.Condominium', verbose_name='Your cond')),
            ],
            options={
                'managed': True,
                'verbose_name': 'News',
                'verbose_name_plural': 'your news',
                'db_table': 'news',
            },
        ),
    ]
