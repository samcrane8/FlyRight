import json
from datetime import timedelta

from django.test import TestCase
from django.urls import reverse

from users.models import IcarusUser as User
from oauth2_provider.models import get_application_model, get_access_token_model
from urllib.parse import urlencode
from django.utils import timezone

login_info = {
        'username': 'user1',
        'password': '12345'
    }

register_info = {
        'username': 'user2',
        'password': '12345',
        'email': "e2@mail.com",
        'first_name': 'Sam',
        'last_name': 'Crane'
    }

user_info = {
    'id': 3,
    "username": "user1",
    "email": "e@mail.com",
    "first_name": "",
    "last_name": "",
    'role': '',
    'picture_url': ''
}

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

    def test_application_registration(self):
        self.client.login(username="user1", password="12345")

        form_data = {
            "name": "Foo app",
            "client_id": "client_id",
            "client_secret": "client_secret",
            "client_type": Application.CLIENT_CONFIDENTIAL,
            "redirect_uris": "http://example.com",
            "authorization_grant_type": Application.GRANT_AUTHORIZATION_CODE,
        }

        response = self.client.post(reverse("oauth2_provider:register"), form_data)
        self.assertEqual(response.status_code, 302)

        app = get_application_model().objects.get(name="Foo app")
        self.assertEqual(app.user.username, "user1")

    def test_application_detail_owner(self):
        self.client.login(username="user1", password="12345")

        response = self.client.get(reverse("oauth2_provider:detail", args=(self.oauth_app.pk,)))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post(reverse('icarus register user'), json.dumps(register_info), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username="user2")
        self.assertTrue(user)

    def test_get_current_user(self):
        auth = self._create_authorization_header(self.access_token.token)
        response = self.client.get(reverse('get current user'), HTTP_AUTHORIZATION=auth)
        self.assertEqual(response.status_code, 200)
        user = json.loads(response.content)['user']
        self.assertEqual(user, user_info)
