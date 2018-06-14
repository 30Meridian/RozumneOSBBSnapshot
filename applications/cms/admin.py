import string
import re

from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from unidecode import unidecode

from system.models import Condominium
from .models import Pages


class PagesAdmin(admin.ModelAdmin):
    list_display = ['title','author','datetime','datetime_update']
    exclude = ['author', 'condominium', 'slug']

    def save_model(self, request, obj, form, change):
        condominium = Condominium.objects.filter(slug=request.session['condominium_slug']).first()
        if request.user in condominium.manager.all():
            obj.author = request.user
            obj.condominium = condominium

            decoded = unidecode(obj.title)
            allow = string.digits + string.ascii_letters + '-_'
            slug = re.sub('[^%s]' % allow, '', decoded).lower()[:24]
            if len(slug) == 0:
                slug = 'slug'
            obj.slug = slug

            i = 0
            while True:
                if Pages.objects.filter(condominium=obj.condominium, slug=obj.slug).count() != 0:
                    i += 1
                    obj.slug = slug + str(i)
                else:
                    obj.save()
                    break


    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(PagesAdmin, self).get_queryset(request)
        else:
            qs = super(PagesAdmin, self).get_queryset(request)
            return qs.filter(condominium=request.session['condominium_id'])

admin.site.register(Pages, PagesAdmin)

list_names_to_translate = [_('Our masters'),_('Our contacts')]
