from django.urls import path

from . import DroneViews

urlpatterns = [
    path('get_user_drones/', DroneViews.get_user_drones, name='get user drones'),
    path('delete_drone/', DroneViews.delete_drone, name='delete drones'),
    path('get_drones_past_missions/', DroneViews.get_drones_past_missions, name='get drones past missions'),
    path('register_drone/', DroneViews.register_drone, name='register drone'),
    path('edit_drone_details/', DroneViews.edit_drone_details, name='edit drone details'),
]
