from django.http import HttpResponse
from oauth2_provider.decorators import protected_resource
from .DroneModel import Drone
from icarus_backend.asset.AssetModel import Asset
import json, uuid
from rest_framework.decorators import api_view


@protected_resource()
@api_view(['GET'])
def get_user_drones(request):
    drones = Drone.objects.filter(owner=request.user)
    dictionaries = [obj.as_dict() for obj in drones]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['POST'])
def delete_drone(request):
    body = request.data
    drone_id_list = [d['id'] for d in body]
    drones = Drone.objects.filter(id__in=drone_id_list).first()
    drones.delete()
    response_data = {'message': 'Drone successfully deleted.'}
    return HttpResponse(json.dumps(response_data), content_type='application/json')


@protected_resource()
@api_view(['POST'])
def get_drones_past_missions(request):
    body = request.data
    drone = Drone.objects.filter(id=body['drone_id']).first()
    assets = Asset.objects.filter(drone=drone)
    dictionaries = [obj.as_dict() for obj in assets]
    return HttpResponse(json.dumps(dictionaries), content_type='application/json')


@protected_resource()
@api_view(['POST'])
def register_drone(request):
    body = request.data
    drone_id = uuid.uuid4()
    name = ''
    if 'name' in body.keys():
        name = body['name']
    new_drone = Drone(id=drone_id, owner=request.user, description=body['description'],
                      manufacturer=body['manufacturer'], type=body['type'],
                      color=body['color'], faa_registration_number=body['faa_registration_number'], name=name)
    new_drone.save()
    response_data = {'message': 'Successfully registered this drone.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['POST'])
def edit_drone_details(request):
    body = request.data
    drone = Drone.objects.filter(id=body['id']).first()
    if drone is None:
        response_data = {'message': 'No drone with that ID exists.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=400)
    if 'description' in body.keys():
        drone.description = body['description']
    if 'manufacturer' in body.keys():
        drone.manufacturer = body['manufacturer']
    if 'type' in body.keys():
        drone.type = body['type']
    if 'color' in body.keys():
        drone.color = body['color']
    if 'name' in body.keys():
        drone.name = body['name']
    if 'faa_registration_number' in body.keys():
        drone.faa_registration_number = body['faa_registration_number']
    drone.save()
    response_data = {'message': 'Drone Successfully updated.'}
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=200)
