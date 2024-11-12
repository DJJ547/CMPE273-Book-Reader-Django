from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class UserRegistrationTest(APITestCase):

    def test_user_registration(self):
        url = reverse('signup')  # Ensure you have this name in your urls.py
        data = {
            "email": "testuser2@example.com",
            "password": "TestPassword123",
            "first_name": "Test",
            "last_name": "User"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['message'], "User registered successfully")

class GoogleLoginTest(APITestCase):

    def test_google_login(self):
        url = reverse('login')  # Ensure you have this name in your urls.py
        data = {
            "token": "YOUR_GOOGLE_ID_TOKEN"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
