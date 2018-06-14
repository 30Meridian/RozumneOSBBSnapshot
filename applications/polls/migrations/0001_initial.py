# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('system', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('choice', models.CharField(verbose_name='user choice', max_length=255)),
            ],
            options={
                'ordering': ['choice'],
            },
        ),
        migrations.CreateModel(
            name='Poll',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('question', models.CharField(verbose_name='Question', max_length=255)),
                ('description', models.TextField(verbose_name='Description', blank=True)),
                ('date_start', models.DateField(verbose_name='date start')),
                ('date_end', models.DateField(verbose_name='date end')),
                ('active', models.BooleanField(default=True, verbose_name='Active')),
                ('archive', models.BooleanField(default=False, verbose_name='Archive')),
                ('condominium', models.ForeignKey(db_column='condominium_ref', verbose_name='Poll condominium', to='system.Condominium')),
            ],
            options={
                'verbose_name': 'Poll',
                'verbose_name_plural': 'Polls',
            },
        ),
        migrations.CreateModel(
            name='Vote',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('choice', models.ForeignKey(verbose_name='vote of choice', to='polls.Choice')),
                ('poll', models.ForeignKey(verbose_name='vote of poll', to='polls.Poll')),
                ('user', models.ForeignKey(verbose_name='vote of user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Vote',
                'verbose_name_plural': 'Votes',
            },
        ),
        migrations.AddField(
            model_name='choice',
            name='poll',
            field=models.ForeignKey(verbose_name='Choice of poll', to='polls.Poll'),
        ),
        migrations.AlterUniqueTogether(
            name='vote',
            unique_together=set([('user', 'poll')]),
        ),
    ]
