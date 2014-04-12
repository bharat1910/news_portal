from django.conf.urls import patterns, url

from news_explorer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^articles$', views.getJson, name='getJson'),
    url(r'^(?P<reqtype>\w+)$', views.initiate_chosen, name='initiate_chosen')
)
