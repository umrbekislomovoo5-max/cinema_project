from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_user(self):
        data = {
            'username': 'umrbek',
            'email': 'umrbek@example.com',
            'password': 'StrongPass123',
            'password2': 'StrongPass123',
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='umrbek').exists())

    def test_register_password_mismatch(self):
        data = {
            'username': 'umrbek2',
            'email': 'umrbek2@example.com',
            'password': 'StrongPass123',
            'password2': 'WrongPass',
        }
        response = self.client.post('/api/auth/register/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_profile_requires_auth(self):
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_profile_authenticated(self):
        user = User.objects.create_user(username='testuser', password='pass')
        self.client.force_authenticate(user=user)
        response = self.client.get('/api/auth/profile/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
