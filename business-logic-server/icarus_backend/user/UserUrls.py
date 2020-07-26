
from django.urls import path
from django.conf.urls import url

from . import UserViews
# Defines the endpoints available on example.com/user/
urlpatterns = [
    path('get_current/', UserViews.icarus_get_current_user, name='get current user'),
    path('get/', UserViews.icarus_get_user, name='get user'),
    path('is_logged_in/', UserViews.icarus_is_logged_in, name='is logged in'),
    path('register_user/', UserViews.icarus_register_user, name='icarus register user'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        UserViews.activate, name='activate'),
    path('update/', UserViews.update_user_info, name='icarus update user'),
    path('forgot_password/', UserViews.forgot_password, name='forgot password'),
    url(r'^reset_password/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        UserViews.reset_password_token, name='reset password'),
    path('change_password/', UserViews.change_password, name='change password'),
]
