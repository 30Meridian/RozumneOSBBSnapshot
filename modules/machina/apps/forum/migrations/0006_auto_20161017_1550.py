# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0005_proxyforumconversationattachment_proxyforumconversationpost_proxyforumconversationtopic_proxyforumco'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ProxyForumConversationAttachment',
        ),
        migrations.DeleteModel(
            name='ProxyForumConversationPost',
        ),
        migrations.DeleteModel(
            name='ProxyForumConversationTopic',
        ),
        migrations.DeleteModel(
            name='ProxyForumConversationTopicPoll',
        ),
        migrations.DeleteModel(
            name='ProxyForumConversationTopicPollOption',
        ),
        migrations.DeleteModel(
            name='ProxyForumConversationTopicPollVote',
        ),
        migrations.DeleteModel(
            name='ProxyForumPermission',
        ),
        migrations.DeleteModel(
            name='ProxyForumProfile',
        ),
        migrations.DeleteModel(
            name='ProxyForumReadTrack',
        ),
        migrations.DeleteModel(
            name='ProxyGroupForumPermission',
        ),
        migrations.DeleteModel(
            name='ProxyTopicReadTrack',
        ),
        migrations.DeleteModel(
            name='ProxyUserForumPermission',
        ),
    ]
