from django.contrib import admin
from django import forms
from .models import Issues, Subcontractors
from system.models import User, Condominium
from django.utils.translation import ugettext_lazy as _

class IssuesStatus(forms.ModelForm):
    CHOICES = (
        (0, 'На модерації'),
        (1, 'Відкрита'),
        (2, 'Виконана'),
        (3, 'Відбракована'),
        (4, 'Прийнята до виконання'),
        (5, 'Запланована'),
        (6, 'Арбітраж'),
    )
    status=forms.ChoiceField(choices=CHOICES)

class IssuesAdmin(admin.ModelAdmin):
    list_display = ['title', 'condominium_ref','created', ]
    exclude = ('parent_task_ref','owner_ref', 'condominium_ref')
    form = IssuesStatus

    def get_readonly_fields(self, request, obj=None):
        if obj is None:
            return []
        return ['title','description','address','owner_ref']
    # readonly_fields = ('title','description','address', 'owner_ref')
    def save_model(self, request, obj, form, change):
        obj.parent_task_ref = Issues.objects.get(id=1)
        if not obj.owner_ref:
            obj.owner_ref = request.user
        obj.condominium_ref = Condominium.objects.get(name=request.session['condominium_name'])
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(IssuesAdmin, self).get_queryset(request)
        else:
            qs = super(IssuesAdmin, self).get_queryset(request)
            return qs.filter(condominium_ref=request.session['condominium_id'])



# admin.site.register(Issues, IssuesAdmin)

class SubcontractorsAdmin(admin.ModelAdmin):
    list_display = ('name', 'condominium_ref')
    exclude = ('condominium_ref',)
    def save_model(self, request, obj, form, change):
        obj.condominium_ref = Condominium.objects.get(name=request.session['condominium_name'])
        obj.save()

    def get_queryset(self, request):
        if request.user.is_superuser:
            return super(SubcontractorsAdmin, self).get_queryset(request)
        else:
            qs = super(SubcontractorsAdmin, self).get_queryset(request)
            return qs.filter(condominium_ref=request.session['condominium_id'])

# admin.site.register(Subcontractors, SubcontractorsAdmin)