from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^articles$', views.articles_list, name="articles_list"),
    url(r'^articles/(?P<id>[0-9]+)$', views.article_detail, name="article_detail"),
    url(r'^articles/(?P<category_slug>[a-zA-Z0-9-_]+)$', views.articles_list, name="articles_by_category"),
    url(r'^like_article$', views.like_article, name='like_article'),
    url(r'^popular_category', views.popular_category, name='popular_category'),
    # url(r'^(?P<id>[0-9]+)$', views.article, name="article"),
    url(r'^lastnews$', views.last_news),
    url(r'^grants', views.grants, name="grants"),
    url(r'^about$', views.about_us, name="about_us"),
    url(r'^contact$', views.contacts, name="contacts"),
    url(r'^team$', views.team, name="team"),
    url(r'^best_practice$', views.best_practice, name="best_practice"),
    url(r'^partners$', views.partners, name="partners"),
    url(r'^search_articles', views.search_articles, name="search_articles"),
    url(r'^gallery/', include('photologue.urls', namespace='photologue')),
]




# article_detail


# best_practice
# partners

# like_articles
# last_grants

# index
# articles_list
# last_articles
# about_us
# contacts
# team
# live_stream