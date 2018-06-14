# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0004_city'),
    ]

    operations = [
        migrations.CreateModel(
            name='CondominiumPosition',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('position', models.CharField(choices=[('chairman', 'Сhairman'), ('vice-chairman', 'Vice-Chairman'), ('secretary', 'Secretary'), ('trustee', 'Trustee'), ('member', 'Member')], verbose_name='position', max_length=16)),
            ],
            options={
                'db_table': 'condominium_position',
            },
        ),
        migrations.AddField(
            model_name='condominium',
            name='city',
            field=models.ForeignKey(default=1, db_column='city', to='system.City', verbose_name='city'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='condominium',
            name='document',
            field=models.FileField(default='', verbose_name='document', upload_to=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='condominiumposition',
            name='condominium',
            field=models.ForeignKey(db_column='condominium', to='system.Condominium', verbose_name='condominium'),
        ),
        migrations.AddField(
            model_name='condominiumposition',
            name='user',
            field=models.ForeignKey(db_column='user', to=settings.AUTH_USER_MODEL, verbose_name='user'),
        ),
    ]
