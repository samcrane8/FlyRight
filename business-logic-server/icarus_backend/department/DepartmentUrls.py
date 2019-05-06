from django.urls import path

from . import DepartmentViews

urlpatterns = [
    path('is_government_official/', DepartmentViews.is_government_official, name='is government official'),
    path('flight_histogram/', DepartmentViews.flight_histogram, name='flight histogram'),
    path('message_jurisdiction/', DepartmentViews.message_jurisdiction, name='message jurisdiction'),
    path('create/', DepartmentViews.create, name='create department'),
    path('get/', DepartmentViews.get, name='get department'),
    path('get_user_departments/', DepartmentViews.get_user_departments, name='get user departments'),
    path('add_airboss/', DepartmentViews.add_airboss, name='add department member'),
    path('remove_airboss/', DepartmentViews.remove_airboss, name='remove department member'),
    path('add_watch_commander/', DepartmentViews.add_watch_commander, name='add watch commander'),
    path('remove_watch_commander/', DepartmentViews.remove_watch_commander, name='remove watch commander'),
    path('info/', DepartmentViews.info, name='department info'),
    path('delete/', DepartmentViews.delete, name='department delete')
]