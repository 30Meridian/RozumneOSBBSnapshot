# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('problems', '0002_statuses'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='items',
            options={'verbose_name_plural': 'Items', 'verbose_name': 'Item'},
        ),
        migrations.AlterModelOptions(
            name='statuses',
            options={'verbose_name_plural': 'Statuses', 'verbose_name': 'Status'},
        ),
        migrations.AlterField(
            model_name='items',
            name='create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='create'),
        ),
        migrations.AlterField(
            model_name='items',
            name='last_update',
            field=models.DateTimeField(auto_now_add=True, verbose_name='last_update'),
        ),
        migrations.AlterField(
            model_name='statuses',
            name='create',
            field=models.DateTimeField(auto_now_add=True, verbose_name='create'),
        ),
        migrations.AlterField(
            model_name='statuses',
            name='deadline',
            field=models.DateTimeField(null=True, blank=True, verbose_name='deadline'),
        ),
        migrations.AlterField(
            model_name='statuses',
            name='owner',
            field=models.ForeignKey(related_name='status_owner', verbose_name='owner', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='statuses',
            name='resolution',
            field=models.CharField(max_length=3000, verbose_name='resolution'),
        ),
        migrations.AlterField(
            model_name='statuses',
            name='status',
            field=models.CharField(choices=[('3', 'waiting_board_decision'), ('2', 'inwork'), ('6', 'reject'), ('1', 'pedding'), ('4', 'waiting_general_meeting'), ('5', 'done')], max_length=15, verbose_name='status'),
        ),
    ]
