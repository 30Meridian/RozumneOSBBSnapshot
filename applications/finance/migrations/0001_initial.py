# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pay_for', models.CharField(max_length=1000)),
                ('datatime_create', models.DateTimeField(auto_now_add=True)),
                ('datetime_pay', models.DateTimeField()),
                ('amount', models.IntegerField()),
                ('user_ref', models.ForeignKey(db_column='user_ref', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
            },
        ),
    ]
