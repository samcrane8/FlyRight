import requests
import json
from icarus_backend.secrets import secrets

is_prod = True

webhook_url = secrets['webhook_url']


def post_health(message):
    if not is_prod:
        return
    r = requests.post(webhook_url, data=json.dumps({"text": message}), headers={'content-type':'application/json'})
    return r

