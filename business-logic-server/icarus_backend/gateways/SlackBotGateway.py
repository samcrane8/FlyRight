import requests, os
import json

is_prod = True

webhook_url = os.environ.get('SLACKBOT_WEBHOOK_URL', '')


def post_health(message):
    if not is_prod:
        return
    r = requests.post(webhook_url, data=json.dumps({"text": message}), headers={'content-type':'application/json'})
    return r

