from django.test import TestCase
from django.urls import reverse
from users.models import IcarusUser as User
from django.contrib.gis.geos import Polygon
from django.utils.dateparse import parse_datetime
import json
from icarus_backend.flight.FlightModel import Flight
from datetime import timedelta
from django.utils import timezone

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


class DepartmentViewTest(TestCase):

    def setUp(self):
        user = User.objects.create_user(username='user1',
                                        email='e@mail.com',
                                        password='12345')
        User.objects.create_user(username='jeffrey',
                                 email='e@mail.com',
                                 password='12345',
                                 role='government_official')
        area_polygon = Polygon(area['features'][0]['geometry']['coordinates'])
        starts_at = parse_datetime(register_info['starts_at'])
        ends_at = parse_datetime(register_info['ends_at'])
        Flight.objects.create(id=1, title=register_info['title'], area=area_polygon,
                              description=register_info['description'], starts_at=starts_at,
                              ends_at=ends_at, type=register_info['type'], created_by=user)

    def test_is_government_official(self):
        login_info = {
            'username': 'user1',
            'password': '12345'
        }
        login_info_gov = {
            'username': 'jeffrey',
            'password': '12345'
        }
        response = self.client.post(reverse('icarus login'), json.dumps(login_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('is government official'))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response, False)
        response = self.client.get(reverse('icarus logout'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('icarus login'), json.dumps(login_info_gov),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(reverse('is government official'))
        self.assertEqual(response.status_code, 200)
        response = json.loads(response.content)
        self.assertEqual(response, True)

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