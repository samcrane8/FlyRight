from datetime import timedelta
import json

from django.utils import timezone
from django.urls import reverse
from django.test import TestCase
from oauth2_provider.models import get_application_model, get_access_token_model
from users.models import IcarusUser as User
from icarus_backend.pilot.PilotModel import Pilot

Application = get_application_model()
AccessToken = get_access_token_model()


class UserViewTest(TestCase):

    def _create_application(self, name, user):
        app = Application.objects.create(
            name=name, redirect_uris="http://example.com",
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_AUTHORIZATION_CODE,
            user=user
        )
        return app

    def setUp(self):
        self.user = User.objects.create_user(username='user1',
                                        email='e@mail.com',
                                        password='12345')
        self.oauth_app = self._create_application("app foo_user 1", self.user)

        self.access_token = AccessToken.objects.create(
            user=self.user,
            scope="read write",
            expires=timezone.now() + timedelta(seconds=300),
            token="secret-access-token-key",
            application=self.oauth_app
        )

    def _create_authorization_header(self, token):
        return "Bearer {0}".format(token)

    def test_register_pilot(self):
        register_info = {
            'username': 'user2',
            'password': '12345',
            'email': "e2@mail.com",
            'remote_pilot_certificate_number': '123',
            'mobile_phone_number': '404-771-8471',
            'first_name': 'Sam',
            'last_name': 'Crane'
        }
        response = self.client.post(reverse('register pilot'), json.dumps(register_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username="user2")
        self.assertTrue(user)

        register_info_fail = {
            'username': 'user3',
            'password': '12345',
            'email': "e3@mail.com",
            'remote_pilot_certificate_number': '123',
            'mobile_phone_number': '404-771-8471',
            'first_name': 'Sam',
        }

        response = self.client.post(reverse('register pilot'), json.dumps(register_info_fail),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_edit_pilot(self):
        register_info = {
            'username': 'user2',
            'password': '12345',
            'email': "e2@mail.com",
            'remote_pilot_certificate_number': '123',
            'mobile_phone_number': '404-771-8471',
            'first_name': 'Sam',
            'last_name': 'Crane'
        }
        response = self.client.post(reverse('register pilot'), json.dumps(register_info),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user2 = User.objects.filter(username="user2").first()
        self.assertTrue(user2)

        access_token2 = AccessToken.objects.create(
            user=user2,
            scope="read write",
            expires=timezone.now() + timedelta(seconds=300),
            token="secret-access-token-key2",
            application=self.oauth_app
        )

        edit_info = {
            'remote_pilot_certificate_number': '404',
            'mobile_phone_number': '123'
        }
        auth = self._create_authorization_header(access_token2.token)
        response = self.client.post(reverse('update pilot'), json.dumps(edit_info),
                                    content_type='application/json', HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)
        pilot = Pilot.objects.filter(remotePilotCertificateNumber="404").first()
        self.assertTrue(pilot)
        self.assertEqual(pilot.mobilePhoneNumber, '123')
