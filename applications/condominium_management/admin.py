# from django.contrib import admin
# from system.models import Condominium, CondominiumModules
# from django.utils.translation import ugettext_lazy as _
#
# from .models import ManagementPages, ProxyCondominium
#
#
# class CondominiumModulesInline(admin.TabularInline):
#     model = CondominiumModules
#     exclude = ['condominium']
#     readonly_fields = ['module']
#     fields = ['module', 'use', 'weight']
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def has_add_permission(self, request):
#         return False
#
#
# class CondominiumProxyAdmin(admin.ModelAdmin):
#     exclude = Condominium._meta.get_all_field_names()
#     inlines = [CondominiumModulesInline]
#
#     def get_queryset(self, request):
#         if request.user.is_superuser:
#             return super(CondominiumProxyAdmin, self).get_queryset(request)
#         else:
#             qs = super(CondominiumProxyAdmin, self).get_queryset(request)
#             return qs.filter(slug=request.session['condominium_slug'])
#
#     def has_add_permission(self, request):
#         return False
#
#
# admin.site.register(ProxyCondominium, CondominiumProxyAdmin)
#
#
# class PagesAdmin(admin.ModelAdmin):
#     list_display = ['title', 'author', 'datetime_update']
#     exclude = ['condominium', 'author']
#
#     def has_add_permission(self, request):
#         return False
#
#     def has_delete_permission(self, request, obj=None):
#         return False
#
#     def save_model(self, request, obj, form, change):
#         condominium = Condominium.objects.filter(slug=request.session['condominium_slug']).first()
#         if request.user in condominium.manager.all():
#             obj.author = request.user
#             obj.condominium = condominium
#             obj.save()
#
#     def get_queryset(self, request):
#         qs = super(PagesAdmin, self).get_queryset(request)
#         condominium = Condominium.objects.filter(slug=request.session['condominium_slug']).first()
#         return qs.filter(condominium=condominium)
#
#
# admin.site.register(ManagementPages, PagesAdmin)
