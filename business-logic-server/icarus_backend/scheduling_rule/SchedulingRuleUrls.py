
from django.urls import path

from . import SchedulingRuleViews

urlpatterns = [
    path('register/', SchedulingRuleViews.register, name='scheduling rule register'),
    path('edit/', SchedulingRuleViews.edit, name='scheduling rule edit'),
    path('get/', SchedulingRuleViews.get, name='scheduling rule get'),
    path('delete/', SchedulingRuleViews.delete, name='scheduling rule delete'),
    path('get_user_rules/', SchedulingRuleViews.get_user_rules, name='scheduling rule get'),
]