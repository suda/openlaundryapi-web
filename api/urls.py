from django.conf.urls import patterns, url

from api import views

urlpatterns = patterns('api.views',
    url(
        regex=r'^$',
        view=views.collect_data,
        name='api-collect_data',
    ),
)
