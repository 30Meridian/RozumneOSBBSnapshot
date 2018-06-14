# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.contrib import admin

from machina.core.db.models import get_model

Post = get_model('forum_conversation', 'Post')
Attachment = get_model('forum_attachments', 'Attachment')

class AttachmentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AttachmentForm, self).__init__(*args, **kwargs)
        self.fields['post'].queryset = Post.objects.filter(topic__forum__condominium=self.current_condominium)


class AttachmentAdmin(admin.ModelAdmin):
    form = AttachmentForm
    list_display = ('id', 'post', 'comment', 'file', )
    list_display_links = ('id', 'post', 'comment', )
    # raw_id_fields = ('post', )

    def get_form(self, request, obj=None, **kwargs):
        form = super(AttachmentAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(AttachmentAdmin, self).get_queryset(request)
        else:
            qs = super(AttachmentAdmin, self).get_queryset(request)
            return qs.filter(post__topic__forum__condominium__slug=request.session['condominium_slug'])


admin.site.register(Attachment, AttachmentAdmin)
