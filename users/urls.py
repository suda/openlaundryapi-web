from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
    url(
        regex=r'^$',
        view=views.UserListView.as_view(),
        name='users-user_list',
    ),
    url(
        regex=r'^login/$',
        view=views.LoginView.as_view(),
        name='users-login',
    ),
    url(
        regex=r'^dashboard/$',
        view=views.DashboardView.as_view(),
        name='users-dashboard',
    ),
    url(
        regex=r'^dashboard/accounts/$',
        view=views.EditAccountsView.as_view(),
        name='users-edit_accounts',
    ),
    url(
        regex=r'^dashboard/edit_profile/$',
        view=views.edit_profile,
        name='users-edit_profile',
    ),
    url(
        regex=r'^(?P<username>[\w.@+-]+)/$',
        view=views.UserProfileView.as_view(),
        name='users-profile',
    ),
)
