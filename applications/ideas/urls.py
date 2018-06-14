from django.conf.urls import url, patterns

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^help$', views.help, name="help"),
    url(r'^rules$', views.rules, name="rules"),
    url(r'^status/+(?P<status>[0-9]+)$',views.list,name="list"),
    url(r'^(?P<idea_id>[0-9]+)$',views.idea,name="idea"),
    url(r'^add$', views.add, name="add"),
    url(r'^test$', views.test,name="test"),
    url(r'^disvote/+(?P<idea_id>[0-9]+)$', views.disvote, name="disvote"),
    url(r'^vote/+(?P<idea_id>[0-9]+)$', views.vote, name="vote"),

    # url(r'^checktimeout/+(?P<secret>[^\>]+)$', views.checktimeout,name="checktimeout"),
    url(r'^checktimeout/+(?P<secret>[0-9]+)$', views.checktimeout, name="checktimeout"),
    url(r'^print/+(?P<idea_id>[0-9]+)$', views.print, name="print"),
]