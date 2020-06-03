from django.contrib.gis.db import models
from users.models import IcarusUser as User


class Pilot(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    remotePilotCertificateNumber = models.TextField()
    mobilePhoneNumber = models.TextField()
    isPhoneNumberAuthenticated = models.BooleanField(default=False)

    def as_dict(self):
        return {
            "user_id": self.user.id,  # TODO Add ID as a One to One field?
            "remote_pilot_certificate_number": self.remotePilotCertificateNumber,
            "mobile_phone_number": self.mobilePhoneNumber
        }
