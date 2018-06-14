from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Articles, Category, Documents, Photo
from .forms import ArticlesAdminForm, AddCategoryForm, UpdateCategoryForm

from unidecode import unidecode
from datetime import datetime


class DocumentsInline(admin.TabularInline):
    model = Documents
    min_num = 0
    extra = 0


class PhotosInline(admin.TabularInline):
    model = Photo
    min_num = 0
    extra = 0


class ArticlesAdmin(admin.ModelAdmin):
    form = ArticlesAdminForm
    inlines = (DocumentsInline, PhotosInline,)
    list_display = ['title', 'full_name', 'time_created', 'publish']

    fields = ('publish', 'title', 'shortdesc', 'text','categories', 'mainimg', 'datetime_publish')
    # exclude = ('author', 'condominium')
    filter_horizontal = ('categories',)

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

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        if obj.datetime_publish is None:
            obj.datetime_publish = datetime.now()
        obj.save()


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug']

    @staticmethod
    def get_slug(name):
        slug = []
        for letter in name:
            if letter == '-' or letter == ' ':
                slug.append('_')
            else:
                slug.append(unidecode(letter))
        return ''.join(slug)

    def add_view(self, request, form_url='', extra_context=None):
        self.form = AddCategoryForm
        return super(CategoriesAdmin, self).add_view(request, form_url, extra_context)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        self.form = UpdateCategoryForm
        return super(CategoriesAdmin, self).change_view(request, object_id, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        name = form.cleaned_data['title']
        if not change:
            obj.slug = self.get_slug(name)
        super(CategoriesAdmin, self).save_model(request, obj, form, change)


admin.site.register(Articles, ArticlesAdmin)
admin.site.register(Category, CategoriesAdmin)
