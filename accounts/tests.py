from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from accounts.utils import get_tokens_for_user
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

class OnboardingTests(APITestCase):

    #foundation for tests by creating user and setting up URLs
     
    def setUp(self):    
        self.user = User.objects.create_user(
            username='testuser', 
            password='password123', 
            email='test@test.com'
        )
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.forget_url = reverse('forget_password')
        self.reset_confirm_url = reverse('reset_confirm')
        self.profile_url = reverse('user_profile')
        self.update_pass_url = reverse('update_password')
        self.logout_url = reverse('logout')

    #SUCCESS PATHS OF THE TESTING.
    
    #user registration test case(temporary user creation)
    def test_registration_success(self):
        data = {"username": "newuser", "email": "new@test.com", "password": "newpassword123"}
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    #user login test case
    def test_login_success(self):
        data = {"username": "testuser", "password": "password123"}
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    #It inject fake identity of user into request headers.
    def test_update_password_authenticated(self):

        # Logged-in password update
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        data = {"new_password": "newsecurepass123"}
        response = self.client.post(self.update_pass_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Password Updated Successfully!")

    def test_reset_password_confirm_success(self):
        #1 - Recovery Confirmation Success
        token = default_token_generator.make_token(self.user)
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        data = {
            "uid": uid,
            "token": token,
            "new_password": "recoveredpass123"
        }
        response = self.client.post(self.reset_confirm_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

     #NEGATIVE PATHS OF THE TESTING.

     # Invalid login attempt for  implementation of try catch block.
    def test_logout_invalid_token(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.post(self.logout_url, {"refresh": "invalid_token"})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
  
    #verifies that UpdatePasswordView correctly detects missing input and returns a validation error instead of processing empty data.
    def test_update_password_no_data(self):
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        response = self.client.post(self.update_pass_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    #forget password with non-existing email(properly handles the User.DoesNotExist)
    def test_forget_password_user_not_found(self):
        response = self.client.post(self.forget_url, {"email": "wrong@test.com"})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    #registration with invalid data
    def test_registration_invalid_data(self):
        response = self.client.post(self.register_url, {"username": ""})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
   
    #utility function correctly generates a valid dictionary of JWT tokens
class UtilsTests(APITestCase):
    def test_get_tokens_for_user_wrapper(self):
        user = User.objects.create_user(username='utiluser', password='pass')
        tokens = get_tokens_for_user(user)
        self.assertIn('access', tokens)