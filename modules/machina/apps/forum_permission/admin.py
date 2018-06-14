# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.contrib import admin
from django import forms

from machina.core.db.models import get_model

from system.models import User

Forum = get_model('forum', 'Forum')
ForumPermission = get_model('forum_permission', 'ForumPermission')
GroupForumPermission = get_model('forum_permission', 'GroupForumPermission')
UserForumPermission = get_model('forum_permission', 'UserForumPermission')


class ForumPermissionAdmin(admin.ModelAdmin):
    search_fields = ('name', 'codename',)
    list_display = ('name', 'codename', 'is_global', 'is_local',)
    list_editables = ('is_global', 'is_local',)

    def has_delete_permission(self, request, obj=None):
        return False


class GroupForumPermissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(GroupForumPermissionForm, self).__init__(*args, **kwargs)
        self.fields['forum'].queryset = Forum.objects.filter(condominium=self.current_condominium)
        self.fields['forum'].required = True


class GroupForumPermissionAdmin(admin.ModelAdmin):
    form = GroupForumPermissionForm
    search_fields = ('permission__name', 'permission__codename', 'group__name',)
    list_display = ('group', 'permission', 'has_perm', )
    list_editables = ('has_perm',)
    # raw_id_fields = ('group',)
    def get_form(self, request, obj=None, **kwargs):
        form = super(GroupForumPermissionAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(GroupForumPermissionAdmin, self).get_queryset(request)
        else:
            qs = super(GroupForumPermissionAdmin, self).get_queryset(request)
            return qs.filter(forum__condominium__slug=request.session['condominium_slug'])

class UserForumPermissionForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForumPermissionForm, self).__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(condominiums=self.current_condominium)
        self.fields['forum'].queryset = Forum.objects.filter(condominium=self.current_condominium)
        self.fields['permission'].required = True
        self.fields['user'].required = True
        self.fields['forum'].required = True

class UserForumPermissionAdmin(admin.ModelAdmin):
    form = UserForumPermissionForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserForumPermissionAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        return form

    search_fields = ('permission__name', 'permission__codename', 'user__username',)
    list_display = ('user', 'permission', 'has_perm', )
    list_editables = ('has_perm',)
    exclude = ('anonymous_user',)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(UserForumPermissionAdmin, self).get_queryset(request)
        else:
            qs = super(UserForumPermissionAdmin, self).get_queryset(request)
            return qs.filter(forum__condominium__slug=request.session['condominium_slug'])
    # raw_id_fields = ('user',)


admin.site.register(ForumPermission, ForumPermissionAdmin)
admin.site.register(GroupForumPermission, GroupForumPermissionAdmin)
admin.site.register(UserForumPermission, UserForumPermissionAdmin)
