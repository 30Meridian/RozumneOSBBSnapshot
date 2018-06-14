from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from datetime import datetime

from system.models import User, Condominium
from .models import News
from .forms import NewsAdminForm

class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm

    list_display = ['title', 'full_name', 'time_created', 'publish', 'public']

    fields = ('publish', 'title', 'shortdesc', 'text', 'mainimg', 'datetime_publish', 'public')
    # exclude = ('author', 'condominium')
    def time_created(self, obj):
        return '{}{}'.format(
            _(datetime.strftime(obj.datetime, '%b')),
            datetime.strftime(obj.datetime, '.%d, %Y, %H:%M'))

    time_created.short_description = _('Datetime')
    time_created.admin_order_field = 'time_created'

    def full_name(self, obj):
        return '{} {}. {}.'.format(obj.author.last_name, obj.author.first_name[:1],
                                   obj.author.middle_name[:1])

    full_name.short_description = _('Author')

    def get_form(self, request, obj=None, **kwargs):
        form = super(NewsAdmin, self).get_form(request, obj, **kwargs)
        form.current_condominium = Condominium.objects.get(id=request.session['condominium_id'])
        return form

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.condominium = Condominium.objects.get(slug=request.session['condominium_slug'])
        if obj.datetime_publish is None:
            obj.datetime_publish = datetime.now()
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(NewsAdmin, self).get_queryset(request)
        else:
            qs = super(NewsAdmin, self).get_queryset(request)
            return qs.filter(condominium=request.session['condominium_id'])

admin.site.register(News, NewsAdmin)
