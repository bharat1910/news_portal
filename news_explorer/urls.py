from django.conf.urls import patterns, url

from news_explorer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^news_articles_by_selection$', views.news_articles_by_selection, name='news_articles_by_selection')
)
