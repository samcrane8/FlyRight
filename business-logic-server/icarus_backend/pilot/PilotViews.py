from rest_framework.decorators import api_view
from django.http import HttpResponse
import json
from django.contrib.sites.shortcuts import get_current_site
from icarus_backend.utils import validate_body
from oauth2_provider.decorators import protected_resource

from .pilotViewSchemas import register_pilot_schema, update_pilot_info_schema
from .PilotController import PilotController
from .PilotData import PilotRegistrationData


@api_view(['POST'])
@validate_body(register_pilot_schema)
def icarus_register_pilot(request):
    body = request.data
    domain = get_current_site(request).domain
    pilot_data = PilotRegistrationData.from_json(body)
    status, response_data = PilotController.register_pilot(pilot_data, domain)
    response_json = json.dumps(response_data)
    return HttpResponse(response_json, content_type="application/json", status=status)


@protected_resource()
@api_view(['GET'])
def get_pilot_data(request):
    id = request.query_params.get('id')
    status, data = PilotController.get_pilot_data(id)
    return HttpResponse(json.dumps(data), content_type="application/json", status=status)


@protected_resource()
@api_view(['POST'])
@validate_body(update_pilot_info_schema)
def update_pilot_info(request):
        parsed_json = request.data
        status, response_data = PilotController.update_info(request.user.id, parsed_json)
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, content_type="application/json", status=status)