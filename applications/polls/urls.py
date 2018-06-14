from django.conf.urls import patterns, url

from polls.views import PollDetailView, PollListView, PollVoteView, checktimeout


urlpatterns = patterns('',
    url(r'^$', PollListView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)$', PollDetailView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/vote/$', PollVoteView.as_view(), name='vote'),
    url(r'^checktimeout/+(?P<secret>[0-9]+)$', checktimeout, name="checktimeout"),
)
