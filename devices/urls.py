from django.conf.urls import patterns, url

from devices import views

urlpatterns = patterns('devices.views',
    url(
        regex=r'^$',
        view=views.DeviceListView.as_view(),
        name='devices-device_list',
    ),
)
