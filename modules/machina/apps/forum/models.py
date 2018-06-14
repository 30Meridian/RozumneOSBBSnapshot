# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from machina.apps.forum.abstract_models import AbstractForum
from machina.core.db.models import model_factory

from django.utils.translation import ugettext_lazy as _

Forum = model_factory(AbstractForum)


#override admin for forum_conversation application
from machina.apps.forum_conversation import models as conv_model


class ProxyForumConversationTopic(conv_model.Topic):
    class Meta:
        proxy = True
        verbose_name = _('Topic(Conversation)')
        verbose_name_plural = _('Topics(Conversation)')

class ProxyForumConversationPost(conv_model.Post):
    class Meta:
        proxy = True
        verbose_name = _(' Post(Conversation)')
        verbose_name_plural = _(' Posts(Conversation)')

#override admin for forum_conversation/forum_attachments application
#override admin for forum_conversation/forum_polls application
from machina.apps.forum_conversation.forum_attachments import models as attachments_model
from machina.apps.forum_conversation.forum_polls import models as polls_model


class ProxyForumConversationAttachment(attachments_model.Attachment):
    class Meta:
        proxy = True
        verbose_name = _(' Attachment(Conversation)')
        verbose_name_plural = _(' Attachments(Conversation)')


class ProxyForumConversationTopicPoll(polls_model.TopicPoll):
    class Meta:
        proxy = True
        verbose_name = _(' TopicPoll(Conversation)')
        verbose_name_plural = _(' TopicPolls(Conversation)')


class ProxyForumConversationTopicPollOption(polls_model.TopicPollOption):
    class Meta:
        proxy = True
        verbose_name = _(' TopicPollOption(Conversation)')
        verbose_name_plural = _(' TopicPollOptions(Conversation)')


class ProxyForumConversationTopicPollVote(polls_model.TopicPollVote):
    class Meta:
        proxy = True
        verbose_name = _(' TopicPollVote(Conversation)')
        verbose_name_plural = _(' TopicPollVotes(Conversation)')

#override admin for forum_member application
from machina.apps.forum_member import models as member_model


class ProxyForumProfile(member_model.ForumProfile):
    class Meta:
        proxy = True
        verbose_name = _(' Forum Profile(Member)')
        verbose_name_plural = _(' Forum Profiles(Member)')

#override admin for forum_permission application
from machina.apps.forum_permission import models as permission_model


class ProxyForumPermission(permission_model.ForumPermission):
    class Meta:
        proxy = True
        verbose_name = _(' Forum Permission(Permission)')
        verbose_name_plural = _(' Forum Permissions(Permission)')


class ProxyGroupForumPermission(permission_model.GroupForumPermission):
    class Meta:
        proxy = True
        verbose_name = _(' Group Forum Permission(Permission)')
        verbose_name_plural = _(' Group Forum Permissions(Permission)')


class ProxyUserForumPermission(permission_model.UserForumPermission):
    class Meta:
        proxy = True
        verbose_name = _(' User Forum Permission(Permission)')
        verbose_name_plural = _(' User Forum Permissions(Permission)')

#override admin for forum_tracking application
from machina.apps.forum_tracking import models as tracking_model


class ProxyForumReadTrack(tracking_model.ForumReadTrack):
    class Meta:
        proxy = True
        verbose_name = _(' Forum Read Track(Tracking)')
        verbose_name_plural = _(' Forum Read Tracks(Tracking)')


class ProxyTopicReadTrack(tracking_model.TopicReadTrack):
    class Meta:
        proxy = True
        verbose_name = _(' Topic Read Track(Tracking)')
        verbose_name_plural = _(' Topic Read Tracks(Tracking)')