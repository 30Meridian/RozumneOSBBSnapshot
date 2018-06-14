from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
  url(r'^$', views.items_index, name='items_index'),
  url(r'^list$', views.items_list, name='items_list'),
  url(r'^(?P<id>[0-9]+)$', views.items_item, name="items_item"),
  url(r'^create$', views.items_create, name='items_create'),
)