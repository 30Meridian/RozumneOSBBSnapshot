# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attachements',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'managed': True,
                'db_table': 'attachements',
            },
        ),
        migrations.CreateModel(
            name='AuthUserWorkFor',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'db_table': 'auth_user_work_for',
            },
        ),
        migrations.CreateModel(
            name='CommentAttachements',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
            ],
            options={
                'managed': True,
                'db_table': 'comment_attachements',
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('title', models.CharField(blank=True, null=True, max_length=512)),
                ('body', models.CharField(blank=True, null=True, max_length=2048)),
                ('attachements', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('block', models.IntegerField()),
            ],
            options={
                'managed': True,
                'db_table': 'comments',
            },
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('type_name', models.CharField(max_length=45)),
                ('size', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'managed': True,
                'db_table': 'documents',
            },
        ),
        migrations.CreateModel(
            name='Files',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('body', models.TextField(max_length=10485760)),
            ],
            options={
                'managed': True,
                'db_table': 'files',
            },
        ),
        migrations.CreateModel(
            name='IssueFiles',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('document_ref', models.ForeignKey(db_column='document_ref', to='defects.Documents')),
            ],
            options={
                'managed': True,
                'db_table': 'issue_files',
            },
        ),
        migrations.CreateModel(
            name='Issues',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('status', models.IntegerField(verbose_name='Status')),
                ('title', models.CharField(verbose_name='Issues title', max_length=255)),
                ('description', models.CharField(verbose_name='Issues description', max_length=2048)),
                ('address', models.CharField(verbose_name='Issues address', max_length=512)),
                ('created', models.DateTimeField(verbose_name='Issues Created', auto_now_add=True)),
                ('condominium_ref', models.ForeignKey(db_column='condominium_ref', verbose_name='Condominium', to='system.Condominium')),
                ('owner_ref', models.ForeignKey(db_column='owner_ref', to=settings.AUTH_USER_MODEL, verbose_name='Owner', blank=True, null=True)),
                ('parent_task_ref', models.ForeignKey(db_column='parent_task_ref', verbose_name='parent_task_ref', to='defects.Issues')),
            ],
            options={
                'verbose_name_plural': 'Issues',
                'verbose_name': 'Issue',
                'managed': True,
                'db_table': 'issues',
            },
        ),
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('subject', models.CharField(blank=True, null=True, max_length=255)),
                ('text', models.CharField(blank=True, null=True, max_length=2048)),
                ('attachments', models.IntegerField()),
                ('hidden_sender', models.IntegerField()),
                ('hidden_rcpt', models.IntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('rcpt_ref', models.ForeignKey(related_name='auth_user_rcpt_ref', db_column='rcpt_ref', to=settings.AUTH_USER_MODEL)),
                ('sender_ref', models.ForeignKey(related_name='auth_user_sender_ref', db_column='sender_ref', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'managed': True,
                'db_table': 'messages',
            },
        ),
        migrations.CreateModel(
            name='Subcontractors',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('name', models.CharField(verbose_name='subcontractor name', max_length=255)),
                ('condominium_ref', models.ForeignKey(db_column='condominium_ref', verbose_name='subcontractor condominium', to='system.Condominium')),
            ],
            options={
                'verbose_name_plural': 'subcontractors',
                'verbose_name': 'subcontractor',
                'managed': True,
                'db_table': 'subcontractors',
            },
        ),
        migrations.AddField(
            model_name='issuefiles',
            name='issue_ref',
            field=models.ForeignKey(db_column='issue_ref', to='defects.Issues'),
        ),
        migrations.AddField(
            model_name='documents',
            name='file_ref',
            field=models.ForeignKey(db_column='file_ref', to='defects.Files'),
        ),
        migrations.AddField(
            model_name='documents',
            name='owner_ref',
            field=models.ForeignKey(db_column='owner_ref', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='comments',
            name='issue_ref',
            field=models.ForeignKey(db_column='issue_ref', to='defects.Issues'),
        ),
        migrations.AddField(
            model_name='comments',
            name='owner_ref',
            field=models.ForeignKey(db_column='owner_ref', to=settings.AUTH_USER_MODEL, blank=True, null=True),
        ),
        migrations.AddField(
            model_name='commentattachements',
            name='comment_ref',
            field=models.ForeignKey(db_column='comment_ref', to='defects.Comments'),
        ),
        migrations.AddField(
            model_name='commentattachements',
            name='document_ref',
            field=models.ForeignKey(db_column='document_ref', to='defects.Documents'),
        ),
        migrations.AddField(
            model_name='authuserworkfor',
            name='subcontractors_id',
            field=models.ForeignKey(db_column='subcontractors_id', to='defects.Subcontractors'),
        ),
        migrations.AddField(
            model_name='authuserworkfor',
            name='user_id',
            field=models.ForeignKey(db_column='user_id', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachements',
            name='document_ref',
            field=models.ForeignKey(db_column='document_ref', to='defects.Documents'),
        ),
        migrations.AddField(
            model_name='attachements',
            name='message_ref',
            field=models.ForeignKey(db_column='message_ref', to='defects.Messages'),
        ),
    ]
