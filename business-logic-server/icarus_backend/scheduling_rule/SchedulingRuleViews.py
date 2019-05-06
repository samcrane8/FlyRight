from django.http import HttpResponse
import json
from oauth2_provider.decorators import protected_resource
from rest_framework.decorators import api_view

from icarus_backend.utils import validate_body
from .SchedulingRuleData import SchedulingRuleData
from .SchedulingRuleController import SchedulingRuleController
from .SchedulingRuleSchemas import SchedulingRuleSchemas


@protected_resource()
@api_view(['POST'])
@validate_body(SchedulingRuleSchemas.register)
def register(request):
    body = request.data
    scheduling_rule_data = SchedulingRuleData.from_json(body)
    status, response_data = SchedulingRuleController.register(scheduling_rule_data, body['flight_id'])
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def get(request):
    flight_id = request.query_params.get('id')
    status, response_data = SchedulingRuleController.get(flight_id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(SchedulingRuleSchemas.edit)
def edit(request):
    body = request.data
    scheduling_rule_data = SchedulingRuleData.from_json(body)
    status, response_data = SchedulingRuleController.edit(scheduling_rule_data, body['flight_id'])
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def delete(request):
    flight_id = request.query_params.get('id')
    status, response_data = SchedulingRuleController.delete(flight_id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def get_user_rules(request):
    status, response_data = SchedulingRuleController.get_user_rules(request.user.id)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)