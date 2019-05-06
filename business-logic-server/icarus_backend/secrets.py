

import json

secrets_file = open('secrets.json')
secrets_string = secrets_file.read()
secrets = json.loads(secrets_string)