from schema import Schema, SchemaError
import json
from django.http import HttpResponse
import base64


def get_basic_auth_header(user, password):
    """
    Return a dict containg the correct headers to set to make HTTP Basic Auth request
    """
    user_pass = "{0}:{1}".format(user, password)
    auth_string = base64.b64encode(user_pass.encode("utf-8"))
    auth_headers = {
        "HTTP_AUTHORIZATION": "Basic " + auth_string.decode("utf-8"),
    }

    return auth_headers


def validate_body(body_schema):
    def real_decorator(f):
        def wrapper(*args, **kwargs):
            request = args[0]
            try:
                if request.method == 'POST':
                    body = request.data
                    schema = Schema([body_schema])
                    schema.validate([body])
            except SchemaError as error:
                response_json = json.dumps({"message": str(error)})
                return HttpResponse(response_json, content_type="application/json", status=401)
            result = f(*args, **kwargs)
            return result
        return wrapper
    return real_decorator


def set_lat_range(lat_val):
    while lat_val < -180 or lat_val > 180:
        if lat_val > 180:
            lat_val -= 180
        elif lat_val < -180:
            lat_val += 180
    return lat_val