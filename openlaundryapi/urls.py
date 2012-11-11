from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.auth.views import logout

admin.autodiscover()

urlpatterns = patterns('',
    url(r'', include('social_auth.urls')),
    url(r'^$', 'openlaundryapi.views.index', name='main'),
    url(r'^landing/$', 'openlaundryapi.views.landing', name='landing'),
    url(r'^logout/$', logout, name='logout', kwargs={'next_page': '/'}),

    url(r'^api/', include('api.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^devices/', include('devices.urls')),

    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^grappelli/', include('grappelli.urls')),
)
