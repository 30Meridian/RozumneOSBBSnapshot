from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.list, name="list"),
    url(r'^(?P<id>[0-9]+)$', views.article, name="article"),
]