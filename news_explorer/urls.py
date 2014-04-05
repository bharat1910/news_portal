from django.conf.urls import patterns, url

from news_explorer import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^new$', views.new, name='new'),
    url(r'^news_explorer/getArticle/(\d+)/(\d+)/(\d+)$', views.initiateArticle, name='initiateArticle'),
    url(r'^news_explorer/getDropDownList/(\d+)$', views.initiateDropDownList, name='initiateDropDownList'),
    url(r'^news_explorer/(?P<person>\d+)/(?P<organization>\d+)/(?P<location>\d+)$', views.initiate, name='initiate'),
)
