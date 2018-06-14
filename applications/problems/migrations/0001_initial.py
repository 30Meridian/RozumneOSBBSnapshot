# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import stdimage.models
import problems.models


class Migration(migrations.Migration):



    operations = [
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('filename', models.CharField(max_length=255)),
                ('create', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('title', models.CharField(max_length=255, verbose_name='Item Title')),
                ('description', models.CharField(max_length=3000, null=True, verbose_name='Item Description', blank=True)),
                ('photo', stdimage.models.StdImageField(null=True, verbose_name='Item Photo', blank=True, upload_to=problems.models.get_file_path)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('last_update', models.DateTimeField(auto_now_add=True)),
                ('condominium_ref', models.ForeignKey(related_name='problems_condominium', to='system.Condominium', verbose_name='Condominium')),
                ('user_ref', models.ForeignKey(related_name='problems_user_ref', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
        ),
        migrations.CreateModel(
            name='Statuses',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('status', models.CharField(choices=[(4, 'waiting_general_meeting'), (3, 'waiting_board_decision'), (5, 'done'), (2, 'inwork'), (6, 'reject'), (1, 'pedding')], max_length=1)),
                ('create', models.DateTimeField(auto_now_add=True)),
                ('deadline', models.DateTimeField(null=True, blank=True)),
                ('resolution', models.CharField(max_length=3000)),
                ('item_ref', models.ForeignKey(related_name='problems_items', to='problems.Items', verbose_name='Item')),
                ('owner', models.ForeignKey(related_name='status_owner', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='files',
            name='item_ref',
            field=models.ForeignKey(related_name='problems_files_items', to='problems.Items', verbose_name='Item'),
        ),
    ]
