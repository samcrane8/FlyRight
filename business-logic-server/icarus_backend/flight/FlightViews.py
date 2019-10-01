from django.http import HttpResponse
import json
from .FlightModel import Flight
from django.utils import timezone
from oauth2_provider.decorators import protected_resource
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.decorators import api_view
from icarus_backend.flight.FlightViewsSchema import FlightViewSchemas
from icarus_backend.utils import validate_body
from .FlightController import FlightController
from .FlightData import FlightData


@protected_resource()
@api_view(['POST'])
def register_flight(request):
    body = request.data
    mission_data = FlightData.from_json(body)
    domain = get_current_site(request).domain
    status, response_data = FlightController.register(mission_data, request.user, domain)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(FlightViewSchemas.get_flight_info_schema)
def get_flight_info(request):
    body = request.data
    mission_id = body['mission_id']
    status, response_data = FlightController.get_flight_info(mission_id, request.user)
    return HttpResponse(json.dumps(response_data), content_type='application/json', status=status)


@protected_resource()
@api_view(['GET', 'POST'])
@validate_body(FlightViewSchemas.get_flights_schema)
def get_flights(request):
    dictionaries = FlightController.get_flights(request.user, request.method, request.data)
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_upcoming_flights(request):
    user = request.user
    _now = timezone.now()
    missions = Flight.objects.filter(created_by=request.user.id, starts_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_past_flights(request):
    _now = timezone.now()
    missions = Flight.objects.filter(created_by=request.user.id, ends_at__lt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_current_flights(request):
    _now = timezone.now()
    missions = Flight.objects.filter(created_by=request.user.id, starts_at__lt=_now,
                                     ends_at__gt=_now)
    dictionaries = [obj.as_dict() for obj in missions]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['POST'])
def delete_flight(request):
    body = request.data
    mission_id = body['mission_id']
    mission_query = Flight.objects.filter(pk=mission_id)
    if len(mission_query) == 0:
        response_data = {'message': 'Mission does not exist.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=401)
    mission = mission_query[0].as_dict()
    if mission['created_by'] == request.user.id:
        mission_query.delete()
        response_data = {'message': 'Mission deleted successfully.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json")
    else:
        response_data = {'message': 'User does not have permissions to delete mission.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=403)


@protected_resource()
@api_view(['POST'])
@validate_body(FlightViewSchemas.edit_flight_schema)
def edit_flight(request):
    body = request.data
    mission_id = body['mission_id']
    title = body['title'] if 'title' in body.keys() else None
    description = body['description'] if 'description' in body.keys() else None
    starts_at = body['starts_at'] if 'starts_at' in body.keys() else None
    ends_at = body['ends_at'] if 'ends_at' in body.keys() else None
    area = body['area'] if 'area' in body.keys() else None
    mission_type = body['type'] if 'type' in body.keys() else None
    mission_data = FlightData(mission_id, title, mission_type, description,
                              starts_at, ends_at, area)
    domain = get_current_site(request).domain
    status, response_data = FlightController.edit(mission_data, request.user, domain)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
def edit_clearance(request):
    body = request.data
    mission_id = body['mission_id']
    state = body['state']
    message = body['message']
    status, response_dict = FlightController.edit_clearance(request.user.id, mission_id, state, message)
    response_json = json.dumps(response_dict)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(FlightViewSchemas.add_drone_to_flight_schema)
def add_drone_to_flight(request):
    body = request.data
    operator_id = body['operator_id'] if body['operator_id'] != 'CURRENT_USER' else request.user.id
    status, response_data = FlightController.add_drone(body['drone_id'], body['mission_id'], operator_id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(FlightViewSchemas.remove_drone_from_flight_schema)
def remove_drone_from_flight(request):
    body = request.data
    status, response_data = FlightController.remove_drone(body['drone_id'], body['mission_id'])
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
def get_flight_drones(request):
    body = request.data
    mission_id = body['mission_id']
    status, response_data = FlightController.get_drones(mission_id)
    return HttpResponse(json.dumps(response_data), content_type='application/json', status=status)
