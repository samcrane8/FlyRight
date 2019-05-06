from icarus_backend.user.UserController import UserController
from icarus_backend.pilot.PilotModel import Pilot
from users.models import IcarusUser as User
from icarus_backend.pilot.PilotData import PilotRegistrationData


class PilotController:

    @staticmethod
    def register_pilot(pilot_data: PilotRegistrationData, domain) -> (int, dict):
        status, message = UserController.register_user(pilot_data.username,
                            pilot_data.email, pilot_data.password,
                            pilot_data.first_name, pilot_data.last_name, domain)
        if status == 200:
            user = User.objects.filter(email=pilot_data.email).first()
            pilot = Pilot(user=user, remotePilotCertificateNumber=pilot_data.remote_pilot_certificate_number,
                          mobilePhoneNumber=pilot_data.mobile_phone_number)
            pilot.save()
            return 200, {'message': 'Successfully registered pilot.'}
        return status, message

    @staticmethod
    def get_pilot_data(id) -> (int, dict):
        pilot = Pilot.objects.filter(user=id).first()
        if not pilot:
            return 400, {'message': 'No pilot with this id exists.'}
        return 200, pilot.as_dict()

    @staticmethod
    def update_info(user_id, pilot_changes) -> (int, dict):
        pilot = Pilot.objects.filter(user_id=user_id).first()
        if 'remote_pilot_certificate_number' in pilot_changes and pilot.remotePilotCertificateNumber \
                != pilot_changes['remote_pilot_certificate_number']:
            pilot.remotePilotCertificateNumber = pilot_changes['remote_pilot_certificate_number']
        if 'mobile_phone_number' in pilot_changes and pilot.mobilePhoneNumber != pilot_changes['mobile_phone_number']:
            pilot.mobilePhoneNumber = pilot_changes['mobile_phone_number']
        pilot.save()
        return 200, {'message': 'Info updated successfully.'}