from django.http import HttpResponse
from django.utils.timezone import is_aware
from django.utils.dateparse import parse_datetime
from django.contrib.gis.geos import Polygon
from oauth2_provider.decorators import protected_resource
from .AirspaceRestrictionModel import AirspaceRestriction
from icarus_backend.asset.AssetModel import Asset
import json, uuid
from rest_framework.decorators import api_view
from icarus_backend.airspace_restriction.AirSpaceRestrictionSchemas import add_airspace_restriction_schema
from icarus_backend.utils import validate_body


@protected_resource()
@api_view(['POST'])
@validate_body(add_airspace_restriction_schema)
def add_airspace_restriction(request):
    body = request.data
    if request.user.role == 'government_official':
        created_by = request.user

        starts_at = parse_datetime(body['starts_at'])
        if not is_aware(starts_at):
            response_data = {'message': 'Starts at has not timezone.'}
            response_json = json.dumps(response_data)
            return HttpResponse(response_json, status=403, content_type="application/json")

        ends_at = parse_datetime(body['ends_at'])
        if not is_aware(ends_at):
            response_data = {'message': 'Ends at has no timezone.'}
            response_json = json.dumps(response_data)
            return HttpResponse(response_json, status=403, content_type="application/json")

        is_constant = body['is_constant']
        _type = body['type']
        description = body['description']

        coordinates = body['area']['features'][0]['geometry']['coordinates']
        if coordinates[0] is not coordinates[-1]:
            coordinates += [coordinates[0]]
        area = Polygon(coordinates)

        new_airspace_restriction = AirspaceRestriction(created_by=created_by, starts_at=starts_at,
                                                       ends_at=ends_at, is_constant=is_constant,
                                                       type=_type, description=description, area=area)

        new_airspace_restriction.save()
        response_data = {'message': 'Successfully created an Airspace Restriction.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=200, content_type="application/json")
    else:
        response_data = {'message': 'Cannot make airspace restriction, not a Government Official.'}
        response_json = json.dumps(response_data)
        return HttpResponse(response_json, status=403, content_type="application/json")
