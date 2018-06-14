# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import stdimage.models
import blog.models
import ckeditor_uploader.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Articles',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True, verbose_name='Datetime')),
                ('datetime_publish', models.DateTimeField(verbose_name='Datetime_publish')),
                ('title', models.CharField(max_length=150, verbose_name='Title')),
                ('shortdesc', models.CharField(max_length=300, verbose_name='Short description')),
                ('text', ckeditor_uploader.fields.RichTextUploadingField(verbose_name='News text')),
                ('mainimg', stdimage.models.StdImageField(upload_to=blog.models.get_file_path, verbose_name='Main img')),
                ('publish', models.BooleanField(verbose_name='Publish')),
                ('youtube_video', models.CharField(max_length='256', blank=True)),

                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL, verbose_name='Author', db_column='author')),
            ],
            options={
                'managed': True,
                'verbose_name_plural': 'your news',
                'verbose_name': 'News',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('slug', models.CharField(max_length=100)),
            ],
            options={
                'managed': True,
                'db_table': '',
            },
        ),
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('article', models.ForeignKey(to='blog.Articles')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='articles',
            name='categories',
            field=models.ManyToManyField(to='blog.Category'),
        ),
    ]
