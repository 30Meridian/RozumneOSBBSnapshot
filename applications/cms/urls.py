from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.pages_list, name='list'),
    url(r'^(?P<path>.*)$', views.show_page, name='page'),
]