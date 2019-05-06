
from django.urls import path

from . import FlightViews

urlpatterns = [
    path('register/', FlightViews.register_flight, name='register flight'),
    path('get/', FlightViews.get_flights, name='get flights'),
    path('get_past/', FlightViews.get_past_flights, name='get past flights'),
    path('get_upcoming/', FlightViews.get_upcoming_flights, name='get upcoming flights'),
    path('get_current/', FlightViews.get_current_flights, name='get current flights'),
    path('get_info/', FlightViews.get_flight_info, name='get flight info'),
    path('delete/', FlightViews.delete_flight, name='delete flight'),
    path('edit_clearance/', FlightViews.edit_clearance, name='edit clearance'),
    path('edit/', FlightViews.edit_flight, name='edit flight details'),
    path('add_drone/', FlightViews.add_drone_to_flight, name='add drone to flight'),
    path('remove_drone/', FlightViews.remove_drone_from_flight, name='remove drone from flight'),
    path('get_drones/', FlightViews.get_flight_drones, name='get flight drones'),
]