from django import forms
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.forms.models import BaseInlineFormSet

from .models import Items, Statuses
from system.models import Condominium

import datetime
# class StatusesForm(forms.ModelForm):
#     def __init__(self, *args, **kwargs):
#         super(StatusesForm, self).__init__(*args, **kwargs)
#
#         self.fields['status'].required = False
#         self.fields['resolution'].required = False

class ItemsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)
        # self.fields['public'].initial = Condominium.objects.get(id=self.current_condominium).public_problems
        if self.add_obj:
            self.fields['description'].widget = forms.widgets.Textarea(
                attrs={'rows': 15, 'style': 'resize: none; width: 90%', })

class StatusesForm(BaseInlineFormSet):

    def _construct_form(self, i, **kwargs):
        form = super(StatusesForm, self)._construct_form(i, **kwargs)
        # if i < 1:
        #     form.empty_permitted = False
        return form

class AddStatusesInline(admin.TabularInline):
    model = Statuses
    formset = StatusesForm
    verbose_name = _("Status")
    verbose_name_plural = _("Add statuses")

    fk_name = "item_ref"
    exclude = ('owner', )
    max_num = 1
    # min_num = 0
    # extra = 0
    # suit_classes = 'suit-tab suit-tab-general'
    def has_change_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class LogStatusesInline(admin.TabularInline):
    model = Statuses
    verbose_name = _("Statuses log")
    verbose_name_plural = _("Statuses log")
    fk_name = "item_ref"
    exclude = ('owner', )
    readonly_fields = ['status', 'deadline', 'resolution', 'owner']
    # suit_classes = 'suit-tab suit-tab-statuses'

    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

class ItemsAdmin(admin.ModelAdmin):
    form = ItemsForm
    model = Items
    inlines = (AddStatusesInline, LogStatusesInline)
    list_display = ('image', 'title', 'full_name', 'time_created', 'time_update', 'public')
    add_exclude = ('user_ref', 'condominium_ref')
    change_exclude = ('photo',)
    list_display_links = ('image', 'title',)

    def get_form(self, request, obj=None, **kwargs):
        form = super(ItemsAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = request.session['condominium_id']
        if obj is None:
            form.add_obj = True
        else:
            form.add_obj = False
        return form

    def image(self, obj):
        if obj.photo:
            return '<img src="/media/%s"/>' % obj.photo.thumbnail
        else:
            return '<img src="/static/img/empty.gif" width="100px"/>'

    image.allow_tags = True
    image.short_description = _('Item Photo')

    def full_name(self, obj):
        return '{} {}. {}.'.format(obj.user_ref.last_name, obj.user_ref.first_name[:1],
                                   obj.user_ref.middle_name[:1])

    def time_created(self, obj):
        return '{}{}'.format(
            _(datetime.datetime.strftime(obj.create, '%b')),
            datetime.datetime.strftime(obj.create, '.%d, %Y, %H:%M'))

    def time_update(self, obj):
        return '{}{}'.format(
            _(datetime.datetime.strftime(obj.last_update, '%b')),
            datetime.datetime.strftime(obj.last_update, '.%d, %Y, %H:%M'))

    time_created.short_description = _('create')
    time_update.short_description = _('last_update')
    time_created.admin_order_field = 'create'
    time_update.admin_order_field = 'last_update'

    full_name.short_description = _('Author')

    def add_view(self, *args, **kwargs):
        self.exclude = getattr(self, 'add_exclude', ())
        return super(ItemsAdmin, self).add_view(*args, **kwargs)

    def change_view(self, *args, **kwargs):
        self.exclude = getattr(self, 'change_exclude', ())
        return super(ItemsAdmin, self).change_view(*args, **kwargs)

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['title', 'user_ref', 'condominium_ref', 'description',]

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(ItemsAdmin, self).get_queryset(request)
        else:
            qs = super(ItemsAdmin, self).get_queryset(request)
            return qs.filter(condominium_ref=request.session['condominium_id'])

    def save_model(self, request, obj, form, change):
        obj.condominium_ref = Condominium.objects.get(slug=request.session['condominium_slug'])
        # obj.owner_id = request.user
        obj.user_ref = request.user
        obj.save()

    def save_formset(self, request, form, formset, change):

        instances = formset.save(commit=False)
        for instance in instances:
            instance.owner = request.user
            instance.save()

        if not change:
            item = Items.objects.get(title=form.cleaned_data['title'],
                                     description=form.cleaned_data['description'],
                                     user_ref=request.user)
                                     # create=datetime.datetime.now())
            try:
                Statuses.objects.get(item_ref=item)
            except:
                Statuses.objects.create(status='pedding', create=datetime.datetime.now(), item_ref=item, owner=request.user)

        formset.save_m2m()


    # suit_form_tabs = (('general', _('General')), ('statuses', _('Statuses log')))
    # fieldsets = [
    #     (None, {
    #         'classes': ('suit-tab', 'suit-tab-general',),
    #         'fields': ['title', 'user_ref', 'condominium_ref']
    #     }),
    #     (None, {
    #         'classes': ('suit-tab', 'suit-tab-statuses',),
    #         'fields': []
    #     }),
    # ]


admin.site.register(Items, ItemsAdmin)
# admin.site.register(Statuses)