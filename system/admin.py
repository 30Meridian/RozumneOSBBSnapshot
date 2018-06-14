import uuid

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext as _
from django import forms
from django.contrib.auth.models import Group

import nested_admin

from .models import ProxyManagementPages

from .models import User, Condominium, ObjectTypes, ObjectRegistry, CondominiumFloor, CondominiumPorch, \
    CondominiumHouse, CondominiumNonResidentialPremise, CondominiumResidentialPremise, CondominiumCommonArea, \
    CondominiumInfrastructure, CondominiumModules
from .forms import LocalizedSelect, HouseAutoGenerationForm
from .utils import generate_house_from_form


class ManagerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ManagerForm, self).__init__(*args, **kwargs)
        self.fields['manager'].queryset = User.objects.filter(condominiums=self.instance.id)
        self.fields['ideas_number_templ'].required = True


class FloorObjectTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(FloorObjectTypeForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = ObjectTypes.objects.filter(category='Floor')

    class Meta:
        widgets = {
            'type': LocalizedSelect(attrs={'class': 'selectpicker'})
        }


class InfrastructureObjectTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(InfrastructureObjectTypeForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = ObjectTypes.objects.filter(category='Infrastructure')

    class Meta:
        widgets = {
            'type': LocalizedSelect(attrs={'class': 'selectpicker'})
        }


class CommonObjectTypeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommonObjectTypeForm, self).__init__(*args, **kwargs)
        self.fields['type'].queryset = ObjectTypes.objects.filter(category='CommonArea')

    class Meta:
        widgets = {
            'type': LocalizedSelect(attrs={'class': 'selectpicker'})
        }


class CondominiumAdmin(admin.ModelAdmin):
    form = ManagerForm
    exclude = ('city',)
    filter_horizontal = ('manager',)
    readonly_fields = ('slug',)
    fields = ('name', 'slug', 'document', 'legal_address', 'description', 'votes', 'problem_days', 'ideas_days',
              'ideas_number_templ', 'manager', 'public_ideas', 'public_news', 'public_polls', 'public_problems')
    list_display = ('name', 'city', 'legal_address', 'datetime_created')

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(CondominiumAdmin, self).get_queryset(request)
        else:
            qs = super(CondominiumAdmin, self).get_queryset(request)
            return qs.filter(slug=request.session['condominium_slug'])

    def has_add_permission(self, request):
        return False


# Inline admin for house

class FloorInlines(nested_admin.NestedStackedInline):
    model = CondominiumFloor
    form = FloorObjectTypeForm
    fk_name = "porch"
    exclude = ('object_registry',)
    max_num = 20
    extra = 0


class PorchAdminInlines(nested_admin.NestedStackedInline):
    model = CondominiumPorch
    fk_name = "house"
    exclude = ('object_registry', 'name', 'lighting_points')
    inlines = [FloorInlines]
    max_num = 10
    extra = 0


class HouseAdmin(nested_admin.NestedModelAdmin):
    inlines = (PorchAdminInlines,)
    form = HouseAutoGenerationForm

    max_floors = forms.Select()

    list_display = ('address', 'area',)
    list_display_links = ('address')

    def get_form(self, request, obj=None, **kwargs):
        form = super(HouseAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['address'].initial = Condominium.objects.get(
            id=request.session['condominium_id']).legal_address
        return form

    def save_model(self, request, obj, form, change):
        generate_house_from_form(request, obj, form)

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(HouseAdmin, self).get_queryset(request)
        else:
            qs = super(HouseAdmin, self).get_queryset(request)
            return qs.filter(condominium=request.session['condominium_id'])


class CommonAreaAdmin(admin.ModelAdmin):
    form = CommonObjectTypeForm
    exclude = ('object_registry',)
    list_display = ('type', 'area')

    def save_model(self, request, obj, form, change):
        reg = ObjectRegistry(condominium_id=request.session['condominium_id'], type=obj.type,
                             user_created=request.user, user_changed=request.user,
                             title='{}, {}-{}'.format(_(str(obj.type)), _('area'), obj.area))
        reg.save()
        obj.object_registry = reg
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(CommonAreaAdmin, self).get_queryset(request)
        else:
            qs = super(CommonAreaAdmin, self).get_queryset(request)
            return qs.filter(object_registry__condominium=request.session['condominium_id'])


class InfrastructureAdmin(admin.ModelAdmin):
    form = InfrastructureObjectTypeForm
    exclude = ('object_registry',)
    list_display = ('type', 'area')

    def save_model(self, request, obj, form, change):
        reg = ObjectRegistry(condominium_id=request.session['condominium_id'], type=obj.type,
                             user_created=request.user, user_changed=request.user,
                             title='{}, {}-{}'.format(_(str(obj.type)), _('area'),
                                                      obj.area))  # str(obj.description[:50]))# _(str(obj.type)))
        reg.save()
        obj.object_registry = reg
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(InfrastructureAdmin, self).get_queryset(request)
        else:
            qs = super(InfrastructureAdmin, self).get_queryset(request)
            return qs.filter(object_registry__condominium=request.session['condominium_id'])


class ResidentialPremiseInline(admin.StackedInline):
    model = CondominiumResidentialPremise
    exclude = ['object_registry', 'house']
    extra = 0

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'floor':
            query = CondominiumFloor.objects.filter(
                porch__house__condominium=request.session['condominium_id'])
        elif db_field.name == 'type':
            query = ObjectTypes.objects.filter(category='CondominiumResidentialPremise')
        else:
            query = super(ResidentialPremiseInline, self).get_field_queryset(db, db_field, request)
        return query


class NonResidentialPremiseInline(admin.StackedInline):
    model = CondominiumNonResidentialPremise
    exclude = ['object_registry', 'house']
    extra = 0

    def get_field_queryset(self, db, db_field, request):
        if db_field.name == 'floor':
            query = CondominiumFloor.objects.filter(
                porch__house__condominium=request.session['condominium_id'])
        elif db_field.name == 'type':
            query = ObjectTypes.objects.filter(category='CondominiumNonResidentialPremise')
        else:
            query = super(NonResidentialPremiseInline, self).get_field_queryset(db, db_field, request)
        return query


class UserAdmin(admin.ModelAdmin):
    fields = ['last_name', 'first_name', 'middle_name', 'phone', 'email']
    inlines = [ResidentialPremiseInline, NonResidentialPremiseInline]

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        if not obj.password:
            obj.set_password('111111')
        obj.username = str(uuid.uuid1())[:16]
        obj.save()

        obj.groups.add(Group.objects.get(name='user'))
        obj.condominiums.add(int(request.session['condominium_id']))
        obj.save()

        return obj

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(UserAdmin, self).get_queryset(request)
        else:
            queryset = super(UserAdmin, self).get_queryset(request)
            return queryset.filter(condominiums=request.session['condominium_id'])


class ProxyCondominium(Condominium):
    class Meta:
        proxy = True
        verbose_name = _('Condominium modules')
        verbose_name_plural = _('Condominium modules')


class CondominiumModulesInline(admin.TabularInline):
    model = CondominiumModules
    exclude = ['condominium']
    readonly_fields = ['module']
    fields = ['module', 'use', 'weight']

    def has_delete_permission(self, request, obj=None):
        return False

    def has_add_permission(self, request):
        return False


class CondominiumProxyAdmin(admin.ModelAdmin):
    exclude = Condominium._meta.get_all_field_names()
    inlines = [CondominiumModulesInline]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(CondominiumProxyAdmin, self).get_queryset(request)
        else:
            qs = super(CondominiumProxyAdmin, self).get_queryset(request)
            return qs.filter(slug=request.session['condominium_slug'])

    def has_add_permission(self, request):
        return False


class PagesAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'datetime_update']
    fields = ['slug', 'title', 'content' ]
    readonly_fields = ['slug',]
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def save_model(self, request, obj, form, change):
        condominium = Condominium.objects.filter(slug=request.session['condominium_slug']).first()
        if request.user in condominium.manager.all():
            obj.author = request.user
            obj.condominium = condominium
            obj.save()

    def get_queryset(self, request):
        qs = super(PagesAdmin, self).get_queryset(request)
        condominium = Condominium.objects.filter(slug=request.session['condominium_slug']).first()
        return qs.filter(condominium=condominium)


admin.site.register(ProxyCondominium, CondominiumProxyAdmin)
admin.site.register(ProxyManagementPages, PagesAdmin)
admin.site.register(Condominium, CondominiumAdmin)
admin.site.register(CondominiumHouse, HouseAdmin)
admin.site.register(CondominiumCommonArea, CommonAreaAdmin)
admin.site.register(CondominiumInfrastructure, InfrastructureAdmin)
admin.site.register(get_user_model(), UserAdmin)
