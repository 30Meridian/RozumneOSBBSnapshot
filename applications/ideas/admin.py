from django.contrib import admin
from django import forms
from django.utils.translation import ugettext_lazy as _
import datetime

from system.models import Condominium
from .forms import IdeaAdminForm
from .models import Ideas, IdeasActivity, IdeasVoices, IdeasStatuses



class ActivityInline(admin.TabularInline):
    model = IdeasActivity
    fk_name = "idea"
    readonly_fields = ('activity', 'datatime', 'user', 'ip', 'idea')
    suit_classes = 'suit-tab suit-tab-activities'

    def get_max_num(self, request, obj=None, **kwargs):
        max_num = 0
        if obj:
            return obj.ideasactivity_set.count()
        return max_num


class IdeasAdmin(admin.ModelAdmin):
    model = Ideas
    inlines = (ActivityInline,)
    form = IdeaAdminForm

    exclude = ('owner_user', 'condominium')
    list_display = ('title','status','time_created', 'full_name', 'voices_count', 'public')
    suit_form_tabs = (('general', _('General')), ('activities', _('Activities') ))

    fieldsets = [
        (None, {
            'classes': ('suit-tab', 'suit-tab-general',),
            'fields': ['title', 'image', 'text', 'status', 'resolution', 'when_approve', 'anonymous', 'public' ]
        }),
        (None, {
            'classes': ('suit-tab', 'suit-tab-activities',),
            'fields': [ ]
        }),
    ]

    def get_form(self, request, obj=None, **kwargs):
        form = super(IdeasAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = Condominium.objects.get(id=request.session['condominium_id'])
        return form

    def full_name(self, obj):
        return '{} {}. {}.'.format(obj.owner_user.last_name, obj.owner_user.first_name[:1],  obj.owner_user.middle_name[:1])


    def voices_count(self, obj):
        return obj.ideasvoices_set.all().count()

    def time_created(self, obj):
        return '{}{}'.format(_(datetime.datetime.strftime(obj.create_date, '%b')), datetime.datetime.strftime(obj.create_date, '.%d, %Y, %H:%M'))

    full_name.short_description = _('Author')
    voices_count.short_description = _('Count of Voices')
    time_created.short_description = _('idea create_date')
    time_created.admin_order_field = 'create_date'

    def get_readonly_fields(self, requset, obj=None):
        if obj is None:
            return []
        return ['title', ]

    def save_model(self, request, obj, form, change):
        obj.condominium = Condominium.objects.get(slug=request.session['condominium_slug'])
        if not obj.owner_user:
            obj.owner_user = request.user
        if obj.status == IdeasStatuses.objects.get(id=2) and not obj.when_approve:
            obj.when_approve = datetime.datetime.now()
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(IdeasAdmin, self).get_queryset(request)
        else:
            qs = super(IdeasAdmin, self).get_queryset(request)
            return qs.filter(condominium=request.session['condominium_id'])


class VoicesAdmin(admin.ModelAdmin):
    model = IdeasVoices
    list_display = ('idea', 'full_name', 'block', 'time_created',)
    exclude = ('idea', 'user', 'ip')
    # ordering = ('-time_created',)
    def full_name(self, obj):
        return '{} {}. {}.'.format(obj.user.last_name, obj.user.first_name[:1],  obj.user.middle_name[:1])

    def time_created(self, obj):
        return '{}{}'.format(_(datetime.datetime.strftime(obj.created, '%b')), datetime.datetime.strftime(obj.created, '.%d, %Y, %H:%M'))

    full_name.short_description = _('Author')
    time_created.short_description = _('created')
    time_created.admin_order_field = 'created'

    def has_add_permission(self, request):
        return False

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(VoicesAdmin, self).get_queryset(request)
        else:
            qs = super(VoicesAdmin, self).get_queryset(request)
            return qs.filter(idea__condominium=request.session['condominium_id'])

admin.site.register(IdeasVoices, VoicesAdmin)
admin.site.register(Ideas, IdeasAdmin)

list_names_to_translate = [_("List"), _("Add idea"), _("Archive")]
