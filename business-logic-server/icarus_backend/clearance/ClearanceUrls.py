from django.urls import path

from . import ClearanceViews

urlpatterns = [
	path('add_clearance/', ClearanceViews.add_clearance, name='add clearance'),
	path('remove_clearance/', ClearanceViews.remove_clearance, name='remove clearance'),
	path('get_clearance_by_clearance_id/', ClearanceViews.get_clearance_by_clearance_id, name='get clearance by clearance_id'),
	path('get_clearance_by_created_by/', ClearanceViews.get_clearance_by_created_by, name='get clearance by created by'),
	path('get_clearance_by_state/', ClearanceViews.get_clearance_by_state, name='get clearance by state'),
	path('get_clearance_by_date/', ClearanceViews.get_clearance_by_date, name='get clearance by date')
]