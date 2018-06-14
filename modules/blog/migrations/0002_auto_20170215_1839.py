# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import system.validators
import blog.models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('file', models.FileField(validators=[system.validators.validate_file_extension], verbose_name='Docs', upload_to=blog.models.get_document_path)),
            ],
        ),
        migrations.RemoveField(
            model_name='articles',
            name='youtube_video',
        ),
        migrations.AlterField(
            model_name='articles',
            name='categories',
            field=models.ManyToManyField(blank=True, to='blog.Category'),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(max_length=100, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='like',
            unique_together=set([('user', 'article')]),
        ),
        migrations.AddField(
            model_name='documents',
            name='article',
            field=models.ForeignKey(to='blog.Articles'),
        ),
    ]
