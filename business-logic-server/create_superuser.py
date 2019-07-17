import os
from icarus_backend.wsgi import *
from icarus_backend.pilot.PilotModel import Pilot
from users.models import IcarusUser as User
from oauth2_provider.models import Application

user = User.objects.filter(username=os.environ.get('SUPERUSER_USERNAME', 'admin')).first()
if not user:
    user = User.objects.create_superuser(os.environ.get('SUPERUSER_USERNAME', 'admin'), os.environ.get('SUPERUSER_EMAIL', 'admin@password.com'), os.environ.get('SUPERUSER_PASSWORD', 'password'))
    pilot = Pilot(user=user, remotePilotCertificateNumber='123',
                          mobilePhoneNumber='123-456-7890')
    user.save()
    pilot.save()

application = Application(client_id='client_id', client_secret='client_secret', client_type='confidential', name='webapp', authorization_grant_type='password')
application.save()