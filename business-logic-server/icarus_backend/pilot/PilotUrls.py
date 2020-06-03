
from django.urls import path

from . import PilotViews
# Endpoints related to pilot management
urlpatterns = [
    path('register/', PilotViews.icarus_register_pilot, name='register pilot'),
    path('get/', PilotViews.get_pilot_data, name='get pilot'),
    path('update/', PilotViews.update_pilot_info, name='update pilot')
]