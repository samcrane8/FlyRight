from django.http import HttpResponse
from rest_framework.decorators import api_view
from oauth2_provider.decorators import protected_resource
import json
from django.utils.dateparse import parse_datetime
from users.models import IcarusUser as User
from icarus_backend.department.DepartmentSchemas import DepartmentSchemas
from icarus_backend.utils import validate_body

from icarus_backend.department.DepartmentController import DepartmentController


@protected_resource()
@api_view(['POST'])
@validate_body(DepartmentSchemas.create)
def create(request):
    current_user = User.objects.filter(id=request.user.id).first()
    if not current_user.is_staff:
        response_data = {'message': 'Must be admin to use this endpoint.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=403, content_type="application/json")
    body = request.data
    name = body['name']
    owner_id = body['owner_id']
    coordinates = body['area']['features'][0]['geometry']['coordinates']
    if coordinates[0] is not coordinates[-1]:
        coordinates += [coordinates[0]]
    status, response_data = DepartmentController.create(name, owner_id, coordinates)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST', 'GET'])
def get(request):
    if request.method == 'GET':
        status, response_data = DepartmentController.get()
    else:  # POST
        coordinates = request.data['area']['features'][0]['geometry']['coordinates']
        if coordinates[0] is not coordinates[-1]:
            coordinates += [coordinates[0]]
        status, response_data = DepartmentController.get(coordinates)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
def add_airboss(request):
    body = request.data
    airboss_id = body['airboss_id']
    name = body['name']
    status, response_data = DepartmentController.add_airboss(name, airboss_id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(DepartmentSchemas.edit)
def edit(request):
    current_user = User.objects.filter(id=request.user.id).first()
    if not current_user.is_staff:
        response_data = {'message': 'Must be admin to use this endpoint.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=403, content_type="application/json")
    body = request.data
    name = body['name']
    new_name = body['new_name']
    coordinates = body['area']['features'][0]['geometry']['coordinates']
    if coordinates[0] is not coordinates[-1]:
        coordinates += [coordinates[0]]
    status, response_data = DepartmentController.edit(name, new_name, coordinates)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
def remove_airboss(request):
    body = request.data
    airboss_id = body['airboss_id']
    name = body['name']
    status, response_data = DepartmentController.remove_airboss(name, airboss_id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
def add_watch_commander(request):
    body = request.data
    watch_commander_id = body['watch_commander_id']
    name = body['name']
    status, response_data = DepartmentController.add_watch_commander(name, watch_commander_id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
def remove_watch_commander(request):
    body = request.data
    watch_commander_id = body['watch_commander_id']
    name = body['name']
    status, response_data = DepartmentController.remove_watch_commander(name, watch_commander_id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def is_government_official(request):
    response_json = json.dumps(DepartmentController.is_department_member(request.user))
    return HttpResponse(response_json, content_type="application/json")


@protected_resource()
@api_view(['POST'])
@validate_body(DepartmentSchemas.flight_histogram_schema)
def flight_histogram(request):
    body = request.data
    start_day = parse_datetime(body['start_day'])
    end_day = parse_datetime(body['end_day'])
    department_id = body['department_id']
    if start_day is None or end_day is None:
        response_json = {'message': 'One or more datetime could not be parsed.'}
        return HttpResponse(json.dumps(response_json), content_type='application/json', status=400)
    status, flight_histogram_data = DepartmentController.flight_histogram(
        department_id, start_day, end_day, request.user)
    return HttpResponse(json.dumps(flight_histogram_data), content_type='application/json', status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(DepartmentSchemas.email_jurisdiction_schema)
def message_jurisdiction(request):
    user = request.user
    body = request.data
    department_name = body['department_name']
    gov_official = DepartmentController.get_user_department_query(user)
    if not gov_official:
        response_json = {'message': 'Must be government official to use this endpoint.'}
        return HttpResponse(json.dumps(response_json), content_type='application/json', status=400)
    DepartmentController.message_pilots(department_name, body['message'])
    response_json = {'message': 'Messages have successfully begun sending.'}
    return HttpResponse(json.dumps(response_json), content_type='application/json')


@protected_resource()
@api_view(['GET'])
def get_user_departments(request):
    user = request.user
    status, response_data = DepartmentController.get_user_department(user)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def info(request):
    id = request.query_params.get('id')
    status, response_data = DepartmentController.info(id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def delete(request):
    id = request.query_params.get('id')
    status, response_data = DepartmentController.delete(id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)

