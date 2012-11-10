from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('api.views',
    url(
        regex=r'^device/(?P<device_id>\w+)/(?P<token>\w+)/$',
        view=views.collect_data,
        name='api-collect_data',
    ),
    url(
        regex=r'^device/(?P<device_id>\w+)/$',
        view=views.device_status,
        name='api-device_status',
    ),
)
