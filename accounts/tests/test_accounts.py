from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

class UserRegistrationTest(APITestCase):

    def setUp(self):
        self.url = '/accounts/register/'
        self.valid_payload = {
            "username": "newuser",
            "password": "somepassword12345",
            "password_confirm": "somepassword12345",
            "email": "newuser@example.com"
        }
        self.invalid_payload = {
            "username": "newuser",
            "password": "invalid",
            "password_confirm": "invalid",
            "email": "invalid-email"
        }

    def test_register_user_success(self):
        response = self.client.post(self.url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, "newuser")

    def test_register_user_with_invalid_data(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)

    def test_register_user_with_password_mismatch(self):
        invalid_password_payload = {
            "username": "user2",
            "password": "somepassword12345",
            "password_confirm": "otherpassword",
            "email": "user2@example.com"
        }
        response = self.client.post(self.url, invalid_password_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    def test_register_user_with_existing_username(self):
        User.objects.create_user(username="existinguser", password="password123")
        
        duplicate_username_payload = {
            "username": "existinguser",
            "password": "newpassword123",
            "password_confirm": "newpassword123",
            "email": "newemail@example.com"
        }
        response = self.client.post(self.url, duplicate_username_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", response.data)
