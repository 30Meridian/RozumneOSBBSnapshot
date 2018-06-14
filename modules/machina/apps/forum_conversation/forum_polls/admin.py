# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from machina.core.db.models import get_model

Forum = get_model('forum', 'Forum')
Topic = get_model('forum_conversation', 'Topic')
TopicPoll = get_model('forum_polls', 'TopicPoll')
TopicPollOption = get_model('forum_polls', 'TopicPollOption')
TopicPollVote = get_model('forum_polls', 'TopicPollVote')

class TopicPollForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TopicPollForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(forum__condominium=self.current_condominium)


#
class TopicPollOptionInline(admin.TabularInline):
    model = TopicPollOption
    extra = 1


class TopicPollOptionAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'poll', 'text',)
    search_fields = ('text',)


class TopicPollAdmin(admin.ModelAdmin):
    form = TopicPollForm
    inlines = (TopicPollOptionInline,)
    list_display = ('topic', 'duration', 'max_options', 'user_changes',)
    list_filter = ('created', 'updated',)
    search_fields = ('topic__subject',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(TopicPollAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TopicPollAdmin, self).get_queryset(request)
        else:
            qs = super(TopicPollAdmin, self).get_queryset(request)
            return qs.filter(topic__forum__condominium__slug=request.session['condominium_slug'])


class TopicPollVoteAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'voter','anonymous_key')
    readonly_fields = ('voter','anonymous_key','poll_option')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TopicPollVoteAdmin, self).get_queryset(request)
        else:
            qs = super(TopicPollVoteAdmin, self).get_queryset(request)
            return qs.filter(poll_option__poll__topic__forum__condominium__slug=request.session['condominium_slug'])
    def has_add_permission(self, request):
        return False

#
admin.site.register(TopicPoll, TopicPollAdmin)
# admin.site.register(TopicPollOption, TopicPollOptionAdmin)
admin.site.register(TopicPollVote, TopicPollVoteAdmin)
