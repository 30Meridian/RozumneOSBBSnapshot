# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_auto_20170215_1839'),
    ]

    operations = [
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
            ],
            options={
                'verbose_name': 'Foto',
                'verbose_name_plural': 'Foto',
            },
        ),
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Category', 'verbose_name_plural': 'Categories', 'managed': True},
        ),
        migrations.AlterModelOptions(
            name='documents',
            options={'verbose_name': 'Document', 'verbose_name_plural': 'Documents'},
        ),
        migrations.AlterField(
            model_name='articles',
            name='categories',
            field=models.ManyToManyField(verbose_name='Categories', to='blog.Category', blank=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.CharField(verbose_name='slug', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(verbose_name='Title', max_length=100),
        ),
        migrations.AddField(
            model_name='photo',
            name='article',
            field=models.ForeignKey(to='blog.Articles'),
        ),
    ]
