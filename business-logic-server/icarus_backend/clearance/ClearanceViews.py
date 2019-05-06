from .ClearanceModel import Clearance
from django.utils import timezone
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json
import uuid
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view


@protected_resource()
@api_view(['POST'])
def add_clearance(request):
    request = request.data
    clearance_id = uuid.uuid4()
    created_by = request['created_by']
    message = request['message']
    state = request['state']
    date = timezone.now()
    object = Clearance(clearance_id = clearance_id, created_by = created_by, message = message, state = state, date = date)
    object.save()

    response_data = {'message': 'Successfully added clearance.'}
    response_json = json.dumps(response_data, cls=DjangoJSONEncoder)
    return HttpResponse(response_json, content_type = "application/json")


@protected_resource()
@api_view(['POST'])
def remove_clearance(request):
    request = request.data
    clearance_id = request['clearance_id'] 
    clearance = Clearance.objects.filter(clearance_id = clearance_id)
    clearance.delete()

    response_data = {'message': 'Successfully removed clearance.'}
    response_json = json.dumps(response_data, cls=DjangoJSONEncoder)
    return HttpResponse(response_json, content_type = "application/json")


@protected_resource()
def get_clearance_by_clearance_id(request):
    request = request.data
    clearance_id = request['clearance_id']
    clearances = Clearance.objects.filter(clearance_id = clearance_id)
    clearance_list = []
    for clearance in clearances:
        clearance_dict = {
            'clearance_id': clearance.clearance_id,
            'created_by': clearance.created_by,
            'message': clearance.message,
            'state': clearance.state,
            'date': clearance.date
        }
        clearance_list.append(clearance_dict)

    response = json.dumps(clearance_list, cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type = 'application/json')


def get_clearance_by_created_by(request):
    request = request.data
    created_by = request['created_by']
    clearances = Clearance.objects.filter(created_by = created_by)
    clearance_list = []
    for clearance in clearances:
        clearance_dict = {
            'clearance_id': clearance.clearance_id,
            'created_by': clearance.created_by,
            'message': clearance.message,
            'state': clearance.state,
            'date': clearance.date
        }
        clearance_list.append(clearance_dict)

    response = json.dumps(clearance_list, cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type = 'application/json')


@protected_resource()
def get_clearance_by_state(request):
    request = request.data
    state = request['state']
    clearances = Clearance.objects.filter(state = state)
    clearance_list = []
    for clearance in clearances:
        clearance_dict = {
            'clearance_id': clearance.clearance_id,
            'created_by': clearance.created_by,
            'message': clearance.message,
            'state': clearance.state,
            'date': clearance.date
        }
        clearance_list.append(clearance_dict)

    response = json.dumps(clearance_list, cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type = 'application/json')


@protected_resource()
def get_clearance_by_date(request):
    request = request.data
    date = request['date']
    clearances = Clearance.objects.filter(date = date)

    clearance_list = []
    for clearance in clearances:
        clearance_dict = {
            'clearance_id': clearance.clearance_id,
            'created_by': clearance.created_by,
            'message': clearance.message,
            'state': clearance.state,
            'date': clearance.date
        }
        clearance_list.append(clearance_dict)

    response = json.dumps(clearance_list, cls=DjangoJSONEncoder)
    return HttpResponse(response, content_type = 'application/json')
