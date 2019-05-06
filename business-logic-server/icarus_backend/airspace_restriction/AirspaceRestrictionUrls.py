from django.urls import path

from . import AirspaceRestrictionViews

urlpatterns = [
    path('add_airspace_restriction/', AirspaceRestrictionViews.add_airspace_restriction, name='add airspace restriction'),
]
