from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'news_portal.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^news_explorer/', include('news_explorer.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
