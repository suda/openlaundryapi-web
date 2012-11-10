from django.conf.urls import patterns, url

from devices import views

urlpatterns = patterns('devices.views',
    url(
        regex=r'^$',
        view=views.DeviceListView.as_view(),
        name='devices-device_list',
    ),
    url(
        regex=r'^(?P<device_id>\w+)/$',
        view=views.DeviceDetailView.as_view(),
        name='devices-device_detail',
    ),
)
