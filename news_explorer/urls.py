from django.conf.urls import patterns, url

from news_explorer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new, name='new'),
    url(r'^initiate$', views.initiate, name='initiate')
)
