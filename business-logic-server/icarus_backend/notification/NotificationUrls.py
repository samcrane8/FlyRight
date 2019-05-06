from django.urls import path

from . import NotificationViews

urlpatterns = [
    path('unread/', NotificationViews.unread, name='icarus notification unread'),
    path('read_all/', NotificationViews.read_all, name='icarus notification read all'),
    path('feed/', NotificationViews.feed, name='icarus notification feed'),
    path('read/', NotificationViews.read, name='icarus read notification'),
]