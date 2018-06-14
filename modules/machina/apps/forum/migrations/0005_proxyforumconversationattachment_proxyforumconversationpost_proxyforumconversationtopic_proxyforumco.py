# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum_conversation', '0005_auto_20160607_0455'),
        ('forum_polls', '0002_auto_20151105_0029'),
        ('forum_member', '0003_auto_20160227_2122'),
        ('forum_tracking', '0002_auto_20160607_0502'),
        ('forum_permission', '0002_auto_20160607_0500'),
        ('forum_attachments', '0001_initial'),
        ('forum', '0004_forum_condominium'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProxyForumConversationAttachment',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' Attachments(Conversation)',
                'verbose_name': ' Attachment(Conversation)',
            },
            bases=('forum_attachments.attachment',),
        ),
        migrations.CreateModel(
            name='ProxyForumConversationPost',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' Posts(Conversation)',
                'verbose_name': ' Post(Conversation)',
            },
            bases=('forum_conversation.post',),
        ),
        migrations.CreateModel(
            name='ProxyForumConversationTopic',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': 'Topics(Conversation)',
                'verbose_name': 'Topic(Conversation)',
            },
            bases=('forum_conversation.topic',),
        ),
        migrations.CreateModel(
            name='ProxyForumConversationTopicPoll',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' TopicPolls(Conversation)',
                'verbose_name': ' TopicPoll(Conversation)',
            },
            bases=('forum_polls.topicpoll',),
        ),
        migrations.CreateModel(
            name='ProxyForumConversationTopicPollOption',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' TopicPollOptions(Conversation)',
                'verbose_name': ' TopicPollOption(Conversation)',
            },
            bases=('forum_polls.topicpolloption',),
        ),
        migrations.CreateModel(
            name='ProxyForumConversationTopicPollVote',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' TopicPollVotes(Conversation)',
                'verbose_name': ' TopicPollVote(Conversation)',
            },
            bases=('forum_polls.topicpollvote',),
        ),
        migrations.CreateModel(
            name='ProxyForumPermission',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' Forum Permissions(Permission)',
                'verbose_name': ' Forum Permission(Permission)',
            },
            bases=('forum_permission.forumpermission',),
        ),
        migrations.CreateModel(
            name='ProxyForumProfile',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' Forum Profiles(Member)',
                'verbose_name': ' Forum Profile(Member)',
            },
            bases=('forum_member.forumprofile',),
        ),
        migrations.CreateModel(
            name='ProxyForumReadTrack',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' Forum Read Tracks(Tracking)',
                'verbose_name': ' Forum Read Track(Tracking)',
            },
            bases=('forum_tracking.forumreadtrack',),
        ),
        migrations.CreateModel(
            name='ProxyGroupForumPermission',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' Group Forum Permissions(Permission)',
                'verbose_name': ' Group Forum Permission(Permission)',
            },
            bases=('forum_permission.groupforumpermission',),
        ),
        migrations.CreateModel(
            name='ProxyTopicReadTrack',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' Topic Read Tracks(Tracking)',
                'verbose_name': ' Topic Read Track(Tracking)',
            },
            bases=('forum_tracking.topicreadtrack',),
        ),
        migrations.CreateModel(
            name='ProxyUserForumPermission',
            fields=[
            ],
            options={
                'proxy': True,
                'verbose_name_plural': ' User Forum Permissions(Permission)',
                'verbose_name': ' User Forum Permission(Permission)',
            },
            bases=('forum_permission.userforumpermission',),
        ),
    ]
