from django.test import TestCase

from core.models import User
from core.serializers import RegisterSerializer

class RegisterSerializerTests(TestCase):
    def test_create_user_with_valid_data(self):
        data = {
            'username': 'alice',
            'email': 'alice@example.com',
            'password': 'complexpass123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid(), msg=serializer.errors)
        user = serializer.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'alice')
        self.assertEqual(user.email, 'alice@example.com')
        self.assertTrue(user.check_password('complexpass123'))

    def test_password_min_length_validation(self):
        data = {
            'username': 'bob',
            'email': 'bob@example.com',
            'password': 'short'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)