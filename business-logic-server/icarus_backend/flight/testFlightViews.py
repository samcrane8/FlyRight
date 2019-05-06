from django.test import TestCase
from django.urls import reverse
from django.contrib.gis.geos import Polygon
from django.utils.dateparse import parse_datetime
from users.models import IcarusUser as User
from icarus_backend.flight.FlightModel import Flight
from icarus_backend.drone.DroneModel import Drone
from datetime import timedelta
from django.utils import timezone
from icarus_backend.clearance.ClearanceModel import Clearance

import json

area = {
    "type": "FeatureCollection",
    "features": [
      {
        "type": "Feature",
        "geometry": {
          "type": "Polygon",
          "coordinates":
            [
              [
                -78.046875,
                13.581920900545844
              ],
              [
                -73.47656249999999,
                -3.162455530237848
              ],
              [
                -60.8203125,
                14.26438308756265
              ],
              [
                -78.046875,
                13.581920900545844
              ]
            ]
        },
        "properties": {}
      }
    ]
  }

register_info = {
  "title": "Venezuela",
  "area": area,
  "description": "testing minimap",
  "starts_at": "2011-10-12T11:45:00+05:00",
  "ends_at": "2011-11-12T11:45:00+05:00",
  "type": "commercial"
}

register_info_2 = {
  "title": "Columbia",
  "area": area,
  "description": "Reconnaissance",
  "starts_at": "2016-10-12T11:45:00+05:00",
  "ends_at": "2016-11-12T11:45:00+05:00",
  "type": "commercial"
}

login_info = {
    'username': 'user1',
    'password': '12345'
}


class MissionViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='user1',
                                 email='e@mail.com',
                                 password='12345')
        area_polygon = Polygon(area['features'][0]['geometry']['coordinates'])
        starts_at = parse_datetime(register_info['starts_at'])
        ends_at = parse_datetime(register_info['ends_at'])
        Clearance.objects.create(clearance_id=0, created_by = 'ray', state='pending', message ='hello', date = "2016-10-12T11:45:00+05:00")
        Flight.objects.create(id=1, title=register_info['title'], area=area_polygon,
                              description=register_info['description'], starts_at=starts_at,
                              ends_at=ends_at, type=register_info['type'], created_by=user, clearance=Clearance.objects.get(clearance_id=0))

    def test_register_mission(self):
        response = self.client.post(reverse('register mission'), json.dumps(register_info_2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 302)
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse('register mission'), json.dumps(register_info_2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Flight.objects.get(title=register_info_2['title']))

    def test_get_missions(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('get missions'))
        response = json.loads(response.content)
        self.assertEqual(response[0]['title'], 'Venezuela')

    def test_get_upcoming_missions(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('get upcoming missions'))
        response = json.loads(response.content)
        self.assertEqual(len(response), 0)

    def test_get_past_missions(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('get past missions'))
        response = json.loads(response.content)
        self.assertEqual(len(response), 1)

    def test_get_current_missions(self):
        user = User.objects.filter(username='user1').first()
        area_polygon = Polygon(area['features'][0]['geometry']['coordinates'])
        _now = timezone.now()
        starts_at = _now - timedelta(days=1)
        ends_at = _now + timedelta(days=1)
        Flight.objects.create(id=2, title=register_info['title'], area=area_polygon,
                              description=register_info['description'], starts_at=starts_at,
                              ends_at=ends_at, type=register_info['type'], created_by=user)
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('get current missions'))
        response = json.loads(response.content)
        self.assertEqual(len(response), 1)

    def test_delete_missions(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        delete_mission_json = {'mission_id': '1'}
        response = self.client.post(reverse('delete missions'), json.dumps(delete_mission_json),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_edit_mission_details(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        edit_mission_details_json = {'mission_id': '1', 'title': 'South Georgia', 'description': "Looking for someone in South Georgia"}
        response = self.client.post(reverse('edit mission details'), json.dumps(edit_mission_details_json),
                                    content_type='application/json')
        mission = Flight.objects.filter(pk=1).first()
        self.assertEqual(mission.title, 'South Georgia')
        self.assertEqual(mission.description, 'Looking for someone in South Georgia')
        self.assertEqual(response.status_code, 200)

    def test_edit_clearance(self):
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        edit_request = {'mission_id':'1', 'created_by':'bob', 'state':'not pending', 'message':'bye bye'}
        response = self.client.post(reverse('edit clearance'), json.dumps(edit_request), content_type='application/json')
        clearance = Clearance.objects.get(clearance_id='0')
        self.assertEqual(clearance.created_by, 'bob')
        self.assertEqual(clearance.state, 'not pending')
        self.assertEqual(clearance.message, 'bye bye')

    def test_add_drone_to_mission(self):
        ri = {
            "description": "fixed-wing, 4\" blades",
            "manufacturer": "DJI",
            "type": "quadrotor",
            "color": "Green"
        }
        user = User.objects.filter(username='user1').first()
        Drone.objects.create(id=1, description=ri['description'], manufacturer=ri['manufacturer'],
                             type=ri['type'], color=ri['color'], owner=user)
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        add_drone_to_mission = { 'drone_id': '1', 'mission_id': '1'}
        response = self.client.post(reverse('add drone to mission'), json.dumps(add_drone_to_mission),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

