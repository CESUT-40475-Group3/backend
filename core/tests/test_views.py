from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from core.models import User

class RegisterAPITests(APITestCase):
    def test_register_endpoint_success(self):
        url = reverse('register')
        payload = {
            'username': 'charlie',
            'email': 'charlie@example.com',
            'password': 'verysecurepassword'
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 201)
        # serializer returns username and email (password is write_only)
        self.assertEqual(resp.data.get('username'), 'charlie')
        self.assertEqual(resp.data.get('email'), 'charlie@example.com')
        self.assertTrue(User.objects.filter(username='charlie').exists())

    def test_register_endpoint_short_password(self):
        url = reverse('register')
        payload = {
            'username': 'dave',
            'email': 'dave@example.com',
            'password': 'short'
        }
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('password', resp.data)

class TokenAPITests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(
            username='eve',
            email='',
            password='strongpassword123'
        )

    def test_login_endpoint_returns_tokens(self):
        url = reverse('token_obtain_pair')
        payload = {'username': 'eve', 'password': 'strongpassword123'}
        resp = self.client.post(url, payload, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIn('refresh', resp.data)
        self.assertIsInstance(resp.data['access'], str)
        self.assertIsInstance(resp.data['refresh'], str)

    def test_refresh_endpoint_returns_new_access(self):
        obtain = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'eve', 'password': 'strongpassword123'},
            format='json'
        )
        refresh = obtain.data.get('refresh')
        resp = self.client.post(reverse('token_refresh'), {'refresh': refresh}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn('access', resp.data)
        self.assertIsInstance(resp.data['access'], str)

    def test_blacklist_logout_prevents_refresh(self):
        obtain = self.client.post(
            reverse('token_obtain_pair'),
            {'username': 'eve', 'password': 'strongpassword123'},
            format='json'
        )
        refresh = obtain.data.get('refresh')

        # Blacklist (logout)
        resp_blacklist = self.client.post(reverse('token_blacklist'), {'refresh': refresh}, format='json')
        self.assertEqual(resp_blacklist.status_code, status.HTTP_200_OK)

        # Attempt to refresh using the same refresh token should fail
        resp_refresh = self.client.post(reverse('token_refresh'), {'refresh': refresh}, format='json')
        self.assertNotEqual(resp_refresh.status_code, status.HTTP_200_OK)
        self.assertIn('detail', resp_refresh.data)
