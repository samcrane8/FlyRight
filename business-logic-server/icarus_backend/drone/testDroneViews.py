from django.test import TestCase
from django.urls import reverse
from users.models import IcarusUser as User
from icarus_backend.drone.DroneModel import Drone
import json

login_info = {
    'username': 'user1',
    'password': '12345'
}

ri = {
      "description" : "fixed-wing, 4\" blades",
      "manufacturer" : "DJI",
      "type": "quadrotor",
      "color": "Green",
      "faa_registration_number": "ABC123"
    }


class DroneViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='user1',
                                 email='e@mail.com',
                                 password='12345')

        Drone.objects.create(id=1, description=ri['description'], manufacturer=ri['manufacturer'],
                             type=ri['type'], color=ri['color'], faa_registration_number=ri['faa_registration_number'], owner=user)

    def test_get_user_drones(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('get user drones'))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response[0]['id'], '1')

    def test_delete_drone(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username='user1').first()
        Drone.objects.create(id=2, description=ri['description'], manufacturer=ri['manufacturer'],
                             type=ri['type'], color=ri['color'], owner=user)
        drones = Drone.objects.filter(owner=user)
        self.assertEqual(len(drones), 2)
        delete_drone_json = { 'drone_id': '2'}
        response = self.client.post(reverse('delete drones'), json.dumps(delete_drone_json),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        drones = Drone.objects.filter(owner=user)
        self.assertEqual(len(drones), 1)

    def test_register_drone(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('register drone'), json.dumps(ri),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username='user1').first()
        drones = Drone.objects.filter(owner=user)
        self.assertEqual(len(drones), 2)

    def test_get_drones_past_missions(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        gdpm_json = {'drone_id': '1', 'mission_id': '1'}
        response = self.client.post(reverse('get drones past missions'), json.dumps(gdpm_json),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_edit_drone_details(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        edit_drone_details_json = {'id': '1', 'manufacturer': 'Icarus', 'color': 'Red'}
        response = self.client.post(reverse('edit drone details'), json.dumps(edit_drone_details_json),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        drone = Drone.objects.filter(id='1')
        self.assertEqual(drone.id, '1')
        self.assertEqual(drone.manufacturer, 'Icarus')
        self.assertEqual(drone.color, 'Red')
        self.assertEqual(len(drone), 1)
