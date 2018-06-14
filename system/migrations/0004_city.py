# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0003_condominium_modules'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('type', models.CharField(max_length=2)),
                ('prefix', models.CharField(max_length=5)),
                ('name', models.CharField(max_length=256)),
                ('specialized_name', models.CharField(max_length=256)),
                ('is_residential', models.BooleanField()),
                ('parent', models.ForeignKey(db_column='parent', to='system.City', null=True)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
                'db_table': 'city',
            },
        ),
        migrations.RemoveField(
            model_name='address',
            name='district',
        ),
        migrations.RemoveField(
            model_name='address',
            name='region',
        ),
        migrations.RemoveField(
            model_name='address',
            name='town',
        ),
        migrations.RemoveField(
            model_name='condominium',
            name='allowed_modules',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='Region',
        ),
        migrations.DeleteModel(
            name='Town',
        ),
    ]
