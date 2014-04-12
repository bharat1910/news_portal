from django.conf.urls import patterns, url

from news_explorer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^articles$', views.getJson, name='getJson'),
    url(r'^click_article$', views.click_article, name='click_article'),
    url(r'^article_content$', views.article_content, name='article_content'),
    url(r'^(?P<reqtype>\w+)$', views.initiate_chosen, name='initiate_chosen')
)
