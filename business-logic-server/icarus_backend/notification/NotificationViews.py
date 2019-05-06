from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view
from .NotificationController import NotificationController
from django.http import HttpResponse
import json


@protected_resource()
@api_view(['GET'])
def unread(request):
    status, body = NotificationController.unread(request.user)
    response_json = json.dumps(body)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def feed(request):
    count = request.query_params.get('count')
    status, body = NotificationController.feed(request.user, count)
    response_json = json.dumps(body)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def read_all(request):
    status, body = NotificationController.read_all(request.user)
    response_json = json.dumps(body)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def read(request):
    notification_id = request.query_params.get('id')
    status, body = NotificationController.read(notification_id)
    response_json = json.dumps(body)
    return HttpResponse(response_json, content_type="application/json", status=status)
