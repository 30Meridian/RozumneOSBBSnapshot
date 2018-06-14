# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import ideas.models
from django.conf import settings
import stdimage.models


class Migration(migrations.Migration):

    dependencies = [
        # ('system', '0017_condominium_problem_days'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ideas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='idea title', max_length=255)),
                ('image', stdimage.models.StdImageField(blank=True, verbose_name='idea image', upload_to=ideas.models.get_file_path)),
                ('text', models.CharField(verbose_name='idea text', max_length=1000)),
                ('claim', models.CharField(verbose_name='idea claim', max_length=1000)),
                ('create_date', models.DateTimeField(verbose_name='idea create_date', auto_now_add=True)),
                ('resolution', models.CharField(blank=True, null=True, verbose_name='idea resolution', max_length=3000)),
                ('when_approve', models.DateTimeField(blank=True, null=True, verbose_name='idea when_approve')),
                ('anonymous', models.BooleanField(verbose_name='idea anonymous')),
                ('condominium', models.ForeignKey(db_column='condominium', verbose_name='idea condominium', to='system.Condominium')),
                ('owner_user', models.ForeignKey(blank=True, db_column='owner_user', null=True, verbose_name='idea owner_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Idea',
                'verbose_name_plural': 'Ideas',
                'managed': True,
                'db_table': 'ideas',
            },
        ),
        migrations.CreateModel(
            name='IdeasActivity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('datatime', models.DateTimeField(verbose_name='activity datatime', auto_now_add=True)),
                ('activity', models.CharField(verbose_name='activity activity', max_length=500)),
                ('ip', models.CharField(verbose_name='activity ip', max_length=500)),
                ('idea', models.ForeignKey(db_column='idea', verbose_name='activity idea', to='ideas.Ideas')),
                ('user', models.ForeignKey(db_column='user', verbose_name='activity user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Activity',
                'verbose_name_plural': 'Activities',
                'managed': True,
                'db_table': 'ideas_activity',
            },
        ),
        migrations.CreateModel(
            name='IdeasStatuses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('title', models.CharField(verbose_name='status title', max_length=50)),
            ],
            options={
                'verbose_name': 'Status',
                'verbose_name_plural': 'Statuses',
                'managed': True,
                'db_table': 'ideas_statuses',
            },
        ),
        migrations.CreateModel(
            name='IdeasVoices',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('block', models.CharField(blank=True, null=True, verbose_name='Voice block', max_length=1)),
                ('created', models.DateTimeField(verbose_name='Voice created', auto_now_add=True)),
                ('ip', models.CharField(verbose_name='Voice ip', max_length=50)),
                ('idea', models.ForeignKey(blank=True, db_column='idea', null=True, verbose_name='Voice idea', to='ideas.Ideas')),
                ('user', models.ForeignKey(blank=True, db_column='user', null=True, verbose_name='Voice user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Voice',
                'verbose_name_plural': 'Voices',
                'ordering': ('idea',),
                'db_table': 'ideas_voices',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='ideas',
            name='status',
            field=models.ForeignKey(db_column='status', verbose_name='idea status', to='ideas.IdeasStatuses'),
        ),
    ]
