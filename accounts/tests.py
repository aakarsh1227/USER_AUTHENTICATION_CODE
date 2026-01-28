from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

#The test class
class OnboardingTests(APITestCase):

    def setUp(self):
        # Create a user to test login and protected routes
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123', 
            email='test@test.com'
        )
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        # Using the name 'forget_password' from your urls.py
        self.forget_url = reverse('forget_password')
#TEst the registration
    def test_registration_success(self):
        data = {
            "username": "newuser", 
            "email": "new@test.com", 
            "password": "newpassword123"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#test login and jwt token
    def test_login_success(self):
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

#Testing the Forget Password Wrapper
    def test_forget_password_logic(self):
        data = {"email": "test@test.com"}
        response = self.client.post(self.forget_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)

#Testing the Security Profile
    def test_protected_profile_security(self):
        profile_url = reverse('user_profile')
        response = self.client.get(profile_url)
        # This confirms our Security Wrapper is working!
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)