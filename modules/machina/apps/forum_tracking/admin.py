# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from machina.core.db.models import get_model

from system.models import User

Forum = get_model('forum', 'Forum')
ForumReadTrack = get_model('forum_tracking', 'ForumReadTrack')
TopicReadTrack = get_model('forum_tracking', 'TopicReadTrack')
Topic = get_model('forum_conversation', 'Topic')


class ForumReadTrackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ForumReadTrackForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(condominiums=self.current_condominium)
        self.fields['forum'].queryset = Forum.objects.filter(condominium=self.current_condominium)


class TopicReadTrackForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TopicReadTrackForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(condominiums=self.current_condominium)
        self.fields['topic'].queryset = Topic.objects.filter(forum__condominium=self.current_condominium)


class ForumReadTrackAdmin(admin.ModelAdmin):
    form = ForumReadTrackForm
    list_display = ('__str__', 'user', 'forum', 'time_mark',)
    list_filter = ('mark_time',)

    def time_mark(self, obj):
        return '{}{}'.format(_(datetime.strftime(obj.mark_time, '%b')),
                             datetime.strftime(obj.mark_time, '.%d, %Y, %H:%M'))

    time_mark.short_description = _('Mark time')
    time_mark.admin_order_field = 'mark_time'

    def get_form(self, request, obj=None, **kwargs):
        form = super(ForumReadTrackAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ForumReadTrackAdmin, self).get_queryset(request)
        else:
            qs = super(ForumReadTrackAdmin, self).get_queryset(request)
            return qs.filter(forum__condominium__slug=request.session['condominium_slug'])


class TopicReadTrackAdmin(admin.ModelAdmin):
    form = TopicReadTrackForm
    list_display = ('__str__', 'user', 'topic', 'time_mark',)
    list_filter = ('mark_time',)

    def time_mark(self, obj):
        return '{}{}'.format(_(datetime.strftime(obj.mark_time, '%b')),
                             datetime.strftime(obj.mark_time, '.%d, %Y, %H:%M'))

    time_mark.short_description = _('Mark time')
    time_mark.admin_order_field = 'mark_time'

    def get_form(self, request, obj=None, **kwargs):
        form = super(TopicReadTrackAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TopicReadTrackAdmin, self).get_queryset(request)
        else:
            qs = super(TopicReadTrackAdmin, self).get_queryset(request)
            return qs.filter(topic__forum__condominium__slug=request.session['condominium_slug'])


admin.site.register(ForumReadTrack, ForumReadTrackAdmin)
admin.site.register(TopicReadTrack, TopicReadTrackAdmin)
