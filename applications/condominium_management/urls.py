from django.conf.urls import include, url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^info$', views.info, name='info'),
    url(r'^info/edit$', views.edit, name='edit'),
    url(r'^cms/', include('cms.urls', namespace='cms')),
    url(r'^house/(?P<house_id>\d+)/$',views.house_info, name='house_info'),
    url(r'^(?P<path>.*)$', views.show_page, name='page'),
]