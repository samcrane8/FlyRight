import os
from icarus_backend.wsgi import *
from icarus_backend.pilot.PilotModel import Pilot
from users.models import IcarusUser as User
from oauth2_provider.models import Application
from icarus_backend.department.DepartmentModel import Department
from django.contrib.gis.geos import Polygon
from icarus_backend.drone.DroneModel import Drone


user = User.objects.filter(username=os.environ.get('SUPERUSER_USERNAME', 'admin')).first()
if not user:
    user = User.objects.create_superuser(os.environ.get('SUPERUSER_USERNAME', 'admin'), os.environ.get('SUPERUSER_EMAIL', 'admin@password.com'), os.environ.get('SUPERUSER_PASSWORD', 'password'))
    
    pilot = Pilot(
        user=user, 
        remotePilotCertificateNumber='123',
        mobilePhoneNumber='123-456-7890'
    )
    user.save()

    airboss = User.objects.filter(id='1')

    department = Department(
        owner = user,
        area = Polygon([
            (33.781572902565564, -84.40757274627684),
            (33.77668601962971, -84.40735816955566),
            (33.774795398883406, -84.4064998626709),
            (33.773118775767486, -84.4019079208374),
            (33.77276204321162, -84.3975305557251),
            (33.771477793711874, -84.39650058746338),
            (33.77137077205131, -84.39229488372803),
            (33.76844546156616, -84.39225196838379),
            (33.7685168117906, -84.39066410064697),
            (33.781572902565564, -84.39096450805664),
            (33.781465893516334, -84.39478397369385),
            (33.782892669846134, -84.3946123123169),
            (33.783142353260104, -84.39701557159424),
            (33.781572902565564, -84.39723014831543),
            (33.781572902565564, -84.40757274627684)
        ]),
        name = "Georgia Tech Police Department",
        # airbosses = user
        # create an airboss template
    )
    department.save()
    department.airbosses.set(airboss)


    drone = Drone(
        id = "c0d59f57-ae0b-47ec-8ec6-a0434468d851",
        owner = user,
        description = "Test Drone Description",
        name = "Test Drone",
        manufacturer = "DJI",
        type = "Rotor",
        faa_registration_number = "123",
        color = "White",
    )
    
    drone.save()
    pilot.save()

application = Application(client_id='client_id', client_secret='client_secret', client_type='confidential', name='webapp', authorization_grant_type='password')
application.save()