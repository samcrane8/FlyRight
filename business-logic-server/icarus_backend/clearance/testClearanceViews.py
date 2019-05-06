from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from icarus_backend.clearance.ClearanceModel import Clearance

import json

class ClearanceViewTest(TestCase):

    def setUp(self):
        Clearance.objects.create(clearance_id = 1, created_by = 'ray', message = 'valid', state = 'pending', date = "2016-10-12T11:45:00+05:00")

    def test_add_clearance(self):
        new_clearance = {
            "created_by": "ray",
            "message": "invalid",
            "state": "pending"
        }
        response = self.client.post(reverse('add clearance'), json.dumps(new_clearance), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(Clearance.objects.get(message = 'invalid'))

    def test_get_clearance_by_clearance_id(self):
        clearance_id = {"clearance_id" : 1}
        response = self.client.post(reverse('get clearance by clearance_id'), json.dumps(clearance_id), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        clearance = json.loads(response.content)
        self.assertEqual(clearance[0]['created_by'], 'ray')
        self.assertEqual(clearance[0]['message'], 'valid')
        self.assertEqual(clearance[0]['state'], 'pending')

    def test_get_clearance_by_created_by(self):
        created_by = {'created_by': 'ray'}
        response = self.client.post(reverse('get clearance by created by'), json.dumps(created_by), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        clearance = json.loads(response.content)
        self.assertEqual(clearance[0]['clearance_id'], '1')

    def test_get_clearance_by_state(self):
        state = {"state": "pending"}
        response = self.client.post(reverse('get clearance by state'), json.dumps(state), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        clearance = json.loads(response.content)
        self.assertEqual(clearance[0]['clearance_id'], '1')

    def test_get_clearance_by_date(self):
        date = {"date": "2016-10-12T11:45:00+05:00"}
        response = self.client.post(reverse('get clearance by date'), json.dumps(date), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        clearance = json.loads(response.content)
        self.assertEqual(clearance[0]['clearance_id'], '1')

    def test_remove_clearance(self):
        clearance_id = {"clearance_id": 1}
        response = self.client.post(reverse('remove clearance'), json.dumps(clearance_id), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(Clearance.objects.all()), 0)
