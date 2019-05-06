
class PilotRegistrationData:

    def __init__(self, username, email, password, remote_pilot_certificate_number,
                 mobile_phone_number, first_name, last_name):
        self.username = username
        self.email = email
        self.password = password
        self.remote_pilot_certificate_number = remote_pilot_certificate_number
        self.mobile_phone_number = mobile_phone_number
        self.first_name = first_name
        self.last_name = last_name

    @staticmethod
    def from_json(json_object):
        username = json_object['username']
        password = json_object['password']
        email = json_object['email']
        mobile_phone_number = json_object['mobile_phone_number']
        remote_pilot_certificate_number = json_object['remote_pilot_certificate_number']
        first_name = json_object['first_name']
        last_name = json_object['last_name']
        return PilotRegistrationData(username, email, password, remote_pilot_certificate_number,
                mobile_phone_number, first_name, last_name)

