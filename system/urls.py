from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.decorators.cache import never_cache
from django.views.i18n import javascript_catalog

from ckeditor_uploader import views as viewsck

from . import views, urls_modules
from .utils import decorated_includes, manage_condominium_permission
from .admin_site import DashboardSite

admin.site = DashboardSite()
admin.autodiscover()

from haystack.views import SearchView
from .forms import CustomSearchForm

urlpatterns = [
    # Index page
    url(r'^$', views.index, name='index'),
    # Condominium namespace
    url(r'^condominium/(?P<condominium_slug>[a-zA-Z0-9-_]+)/', include(urls_modules, namespace='condominium')),

    url(r'^search/', SearchView(form_class=CustomSearchForm), name='haystack_search'),
    # Admin namespace
    url(r'^manage/', decorated_includes(manage_condominium_permission, include(admin.site.urls))),
    # Accounts namespace
    url(r'^accounts/', include('allauth.urls')),
    url(r'^markdown/', include('django_markdown.urls')),
    url(r'^about/', views.about),
    url(r'^help/', views.help_page),
    url(r'^contacts', views.contacts),
    url(r'^instructions/', views.instructions),
    url(r'^load_coordinates$', views.load_condominium_coordinates, name='load_coordinates'),
    # Not sorted urls
    # TODO sort this urls in personal namespaces later. If it's possible.
    # url(r'^regions/', views.regions, name="regions"),
    url(r'^confirmyouremail',views.confirmyouremail),
    url(r'^profile/karma/+(?P<user_id>[0-9]+)',views.karma, name="karma"),
    url(r'^profile/+(?P<user_id>[0-9]+)$',views.profile, name="profile"),
    url(r'^profile/+(?P<user_id>[0-9]+)/edit/$', views.profile_edit, name='profile-edit'),
    url(r'^profile/+(?P<user_id>[0-9]+)/add_residence/$', views.residential_premise_create,
        name='residential-premise-create'),
    url(r'^profile/+(?P<user_id>[0-9]+)/add_non_residence/$', views.non_residential_premise_create,
        name='non-residential-premise-create'),
    url(r'^delete_residence/+(?P<pk>[0-9]+)$', views.residential_premise_delete,
        name='residential_premise_delete'),
    url(r'^delete_non_residence/+(?P<pk>[0-9]+)$', views.non_residential_premise_delete,
        name='non_residential_premise_delete'),
    url(r'^profile/+(?P<user_id>[0-9]+)/manage_utilites/$', views.manage_utilities, name='utilities-manage'),
    url(r'^profile/+(?P<user_id>[0-9]+)/condominium-update/$', views.update_condominiums, name='condominium_update'),
    url(r'^profile/userban/+(?P<user_id>[0-9]+)/+(?P<status>[0-9]+)',views.userban, name="userban"),
    url(r'^ckeditor/upload/', viewsck.upload, name='ckeditor_upload'),
    url(r'^ckeditor/browse/', never_cache(viewsck).browse, name='ckeditor_browse'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':False}),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':False}),
    url(r'^condominiumactivesearch$', views.condominium_active_search),
    url(r'^newsletter/', include('newsletter.urls')),
    url(r'^managechoose/(?P<condominium_slug>[a-zA-Z0-9-_]+)/', views.redirect_to_manage),
    url(r'^nested_admin/', include('nested_admin.urls')),
    url(r'^search', include('haystack.urls')),
    url(r'^condactivesearchformanage$', views.condominium_active_search_for_manage),
    url(r'^jsi18n/$', javascript_catalog, urls_modules.js_info_dict, name='javascript-catalog'),
    url(r'^filter-cities$', views.filter_cities, name='filter-cities'),
    url(r'^filter-condominiums', views.filter_condominiums, name='filter-condominiums'),

    # Blog
    url(r'^index/', include('blog.urls', namespace='blog')),

]