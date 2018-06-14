# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from machina.core.db.models import get_model
from machina.models.fields import MarkupTextField
from machina.models.fields import MarkupTextFieldWidget


from system.models import User
ForumProfile = get_model('forum_member', 'ForumProfile')

class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(condominiums=self.current_condominium)

class ForumProfileAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ('id', 'user', 'posts_count', )
    list_filter = ('posts_count', )
    list_display_links = ('id', 'user', )
    readonly_fields = ('posts_count',)
    # raw_id_fields = ('user', )
    search_fields = ('user__username',)

    formfield_overrides = {
        MarkupTextField: {'widget': MarkupTextFieldWidget(attrs={'rows': 15, 'style': 'resize: none; width: 90%'})},
    }

    def get_form(self, request, obj=None, **kwargs):
        form = super(ForumProfileAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ForumProfileAdmin, self).get_queryset(request)
        else:
            qs = super(ForumProfileAdmin, self).get_queryset(request)
            return qs.filter(user__condominiums__slug=request.session['condominium_slug'])


admin.site.register(ForumProfile, ForumProfileAdmin)
