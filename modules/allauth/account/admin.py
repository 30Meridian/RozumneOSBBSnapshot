from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from django.contrib.auth.admin import GroupAdmin
from django import forms
admin.site.unregister(Site)
admin.site.unregister(Group)
from system.models import User, Condominium, ObjectRegistry

from .models import ProxyGroup, ProxyUser

class ObjectRegistryForm(forms.ModelForm):
    phone = forms.RegexField(regex=r'^\+?\d[\d\(?\)?\s-]{4,18}$',
                             label=_("Phone"), help_text=_('Please input only digits'))
    cond_manager = forms.BooleanField(help_text=_('Designates whether the user can be manager of current condominium'),
                                      label=_('Condominium manager'))
    def __init__(self, *args, **kwargs):
        super(ObjectRegistryForm, self).__init__(*args, **kwargs)
        # self.fields['owned'].queryset = ObjectRegistry.objects.filter(condominium=self.current_condominium.id)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        # self.fields['owned'].required = False
        self.fields['cond_manager'].required = False

        if self.current_user in self.current_condominium.manager.all():
            self.fields['cond_manager'].initial = True

    class Meta:
        help_texts = {
            'owned': _('Condominium number/ Object number and Title.'),
        }


class UserAdmin(admin.ModelAdmin):

    form = ObjectRegistryForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(UserAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = Condominium.objects.get(id=request.session['condominium_id'])
        form.current_user = User.objects.get(id=obj.id)
        return form

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(UserAdmin, self).get_queryset(request)
        else:
            qs = super(UserAdmin, self).get_queryset(request)
            return qs.filter(condominiums__slug=request.session['condominium_slug'])

    def full_name(obj):
        return '{} {} {}'.format(obj.last_name, obj.first_name,  obj.middle_name)

    def condominiums_list(obj):
        q = Condominium.objects.filter(user = obj.id ).values_list('name', flat=True)
        return ", ".join(q)

    def save_model(self, request, obj, form, change):
        current_user = User.objects.get(id=obj.id)
        current_cond = Condominium.objects.get(slug=request.session['condominium_slug'])
        if form.cleaned_data['cond_manager']:
            current_cond.manager.add(current_user)
        else:
            current_cond.manager.remove(current_user)
        obj.save()

    full_name.short_description = _('Full name')
    condominiums_list.short_description = _("Condominiums")

    list_display = (full_name, 'email', 'phone',  condominiums_list)
    exclude = ('user_permissions','password','username',)
    filter_horizontal = ('groups', 'condominiums', 'owned')
    fieldsets = (
        (_('General information'), {
            'fields': ('first_name', 'last_name', 'middle_name', 'phone', 'email',)
                                    }),
        (_('About Condominium'), {
            'fields': ('condominiums', )
                                    }),
        (_('User status'), {
            'fields': ('groups', 'is_staff', 'cond_manager',)
                                    }),
        (_('User activity'), {
            'fields': ('is_active', 'date_joined')
                                    }),
        )

    def has_add_permission(self, request):
        return False



admin.site.register(ProxyUser, UserAdmin)
#
admin.site.register(ProxyGroup, GroupAdmin)
