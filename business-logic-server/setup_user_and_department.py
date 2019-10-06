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
            (34.994003757575776, -85.62744140625),
            (32.69486597787505, -85.14404296875),
            (32.602361666817515, -85.089111328125),
            (32.491230287947594, -84.979248046875),
            (32.36140331527543, -85.01220703125),
            (32.27784451498272, -84.91333007812499),
            (32.24068253457369, -84.91333007812499),
            (32.11980111179328, -85.05615234375),
            (32.02670629333614, -85.05615234375),
            (31.85889704445453, -85.15502929687499),
            (31.606609719226917, -85.078125),
            (31.23159167205059, -85.1220703125),
            (30.987027960280326, -85.001220703125),
            (30.704058230919504, -84.91333007812499),
            (30.56226095049944, -82.276611328125),
            (30.44867367928756, -82.19970703125),
            (30.391830328088137, -82.24365234375),
            (30.372875188118016, -82.078857421875),
            (30.543338954230222, -82.001953125),
            (30.637912028341123, -82.0458984375),
            (30.751277776257812, -82.0458984375),
            (30.789036751261136, -81.968994140625),
            (30.845647420182598, -81.93603515625),
            (30.779598396611537, -81.88110351562499),
            (30.732392734006083, -81.73828125),
            (30.675715404167743, -81.463623046875),
            (30.968189296794247, -81.38671875),
            (31.287939892641734, -81.298828125),
            (31.5504526754715, -81.15600585937499),
            (31.68143311662596, -81.123046875),
            (32.01739159980399, -80.826416015625),
            (32.08722870829662, -81.0955810546875),
            (32.23603621746476, -81.15600585937499),
            (32.31499127724556, -81.112060546875),
            (32.4263401615464, -81.199951171875),
            (32.46806060917602, -81.19445800781249),
            (32.56996256044998, -81.2933349609375),
            (32.62549671451373, -81.4141845703125),
            (32.82421110161336, -81.43615722656249),
            (32.95797741405952, -81.5130615234375),
            (33.01326987686983, -81.5130615234375),
            (33.10534697199519, -81.6339111328125),
            (33.169743600216165, -81.7767333984375),
            (33.4039312002347, -81.93603515625),
            (33.56428403679499, -82.056884765625),
            (33.637489243170826, -82.21618652343749),
            (33.75174787568194, -82.24365234375),
            (33.96614226559745, -82.5567626953125),
            (34.17999758688084, -82.7325439453125),
            (34.28445325435288, -82.75451660156249),
            (34.37517887533528, -82.8424072265625),
            (34.488447837809304, -82.8753662109375),
            (34.48392002731987, -83.0401611328125),
            (34.610605760914666, -83.177490234375),
            (34.69646117272349, -83.3477783203125),
            (34.786739162702524, -83.3258056640625),
            (35.003003395276714, -83.1060791015625),
            (34.994003757575776, -85.62744140625)
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