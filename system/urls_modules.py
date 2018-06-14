from django.conf.urls import include, url

from machina.app import board
from filemanager import path_end

from . import views
from .utils import decorated_includes, forum_condominium_permission


urlpatterns = [
    url(r'^$', views.redirect_to_summary, name='summary'),
    url(r'^home$', views.index_condominium, name='home'),
    url(r'^ourmasters$', views.ourmasters, name='our_masters'),
    url(r'^tariffs$', views.tariffs, name='tariffs'),
    url(r'^people$', views.people, name='people'),
    url(r'^info/+(?P<url_param>[a-z]+)$', views.getDocums, name='info'),
    url(r'^documents/' + path_end, views.document_view, name='documents'),

    # Namespaces
    url(r'^forum/', decorated_includes(forum_condominium_permission, include(board.urls))),
    url(r'^management/', include('condominium_management.urls', namespace='management')),
    url(r'^defects/', include('defects.urls', namespace='defects')),
    url(r'^news/', include('news.urls', namespace='news')),
    url(r'^ideas/', include('ideas.urls', namespace='ideas')),
    url(r'^moderators/', views.moderators, name='moderators'),
    url(r'^rating/', views.rating, name='rating'),
    url(r'^polls/', include('polls.urls', namespace='polls')),
    url(r'^problems/', include('problems.urls', namespace='problems')),

    # Broken link
    url(r'^(?P<broken_link>.*)', views.errorPage, name='error'),
]

js_info_dict = {
    'packages': (
        'system',
        'defects',
        'news',
        'ideas',
        'polls',
        'modules.allauth.account',
        'condominium_management',
        'cms'
    )}