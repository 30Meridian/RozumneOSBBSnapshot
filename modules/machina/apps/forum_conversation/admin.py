# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django import forms
from datetime import datetime
from django.utils.translation import ugettext_lazy as _
from machina.core.db.models import get_model
from machina.models.fields import MarkupTextField
from machina.models.fields import MarkupTextFieldWidget

from system.models import User

Forum = get_model('forum', 'Forum')
Attachment = get_model('forum_attachments', 'Attachment')
Post = get_model('forum_conversation', 'Post')
Topic = get_model('forum_conversation', 'Topic')


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 0

class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['topic'].queryset = Topic.objects.filter(forum__condominium=self.current_condominium)

class PostAdmin(admin.ModelAdmin):

    form = PostForm
    inlines = [AttachmentInline, ]
    list_display = ('__str__', 'topic', 'poster', 'time_updated', 'approved')
    exclude = ('anonymous_key','username', 'poster_ip')
    list_filter = ('created', 'updated')
    # raw_id_fields = ('poster', )
    search_fields = ('content',)
    list_editable = ('approved',)
    readonly_fields = ('poster',)

    formfield_overrides = {
        MarkupTextField: {'widget': MarkupTextFieldWidget(attrs={'rows': 15, 'style': 'resize: none; width: 100%'})},
    }

    def time_updated(self, obj):
        return '{}{}'.format(_(datetime.strftime(obj.updated, '%b')),
                             datetime.strftime(obj.updated, '.%d, %Y, %H:%M'))

    time_updated.short_description = _('Update date')
    time_updated.admin_order_field = 'updated'

    def get_form(self, request, obj=None, **kwargs):
        form = super(PostAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form
    #
    def save_model(self, request, obj, form, change):
        if obj.poster is None:
            obj.poster = request.user
            obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(PostAdmin, self).get_queryset(request)
        else:
            qs = super(PostAdmin, self).get_queryset(request)
            return qs.filter(topic__forum__condominium=request.session['condominium_id'])

class TopicForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TopicForm, self).__init__(*args, **kwargs)
        self.fields['forum'].queryset = Forum.objects.filter(condominium=self.current_condominium)
        self.fields['subscribers'].queryset = User.objects.filter(condominiums=self.current_condominium)
#

class TopicAdmin(admin.ModelAdmin):
    form = TopicForm
    list_display = (
        'subject', 'forum', 'time_created', 'first_post', 'last_post', 'posts_count', 'approved')
    list_filter = ('created', 'updated',)
    # raw_id_fields = ('poster', 'subscribers', )
    search_fields = ('subject',)
    list_editable = ('approved',)
    filter_horizontal = ('subscribers',)
    readonly_fields = ('poster', 'slug')

    def time_created(self, obj):
        return '{}{}'.format(_(datetime.strftime(obj.created, '%b')),
                             datetime.strftime(obj.created, '.%d, %Y, %H:%M'))

    time_created.short_description = _('Creation date')
    time_created.admin_order_field = 'created'

    def get_form(self, request, obj=None, **kwargs):
        form = super(TopicAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    def save_model(self, request, obj, form, change):
        if obj.poster is None:
            obj.poster = request.user
            obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(TopicAdmin, self).get_queryset(request)
        else:
            qs = super(TopicAdmin, self).get_queryset(request)
            return qs.filter(forum__condominium=request.session['condominium_id'])
#
admin.site.register(Topic, TopicAdmin)
admin.site.register(Post, PostAdmin)
