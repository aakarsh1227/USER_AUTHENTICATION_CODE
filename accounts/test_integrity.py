from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

class SystemIntegrityTests(APITestCase):

    def setUp(self):
        # Create the initial state
        self.email = "owner@example.com"
        self.user = User.objects.create_user(
            username='owner', 
            email=self.email, 
            password='old_password123'
        )

    def test_full_password_recovery_integrity(self):
        
        #Tests the integrity of the entire (Recovery Flow). Workflow: Request Token - Use Token - Login with New Pass.
        
        # 1 Request a recovery token
        forget_url = reverse('forget_password')
        forget_res = self.client.post(forget_url, {"email": self.email})
        
        self.assertEqual(forget_res.status_code, 200)
        token = forget_res.data['token']
        uid = forget_res.data['uid']

        # 2 Use that token to set a new password
        confirm_url = reverse('reset_confirm')
        new_pass = "brand_new_secure_pass_2026"
        confirm_res = self.client.post(confirm_url, {
            "uid": uid,
            "token": token,
            "new_password": new_pass
        })
        
        self.assertEqual(confirm_res.status_code, 200)
        self.assertEqual(confirm_res.data['message'], "Password reset successfully!")

        # 3 Try to login with the NEW password
        login_url = reverse('login')
        login_res = self.client.post(login_url, {
            "username": "owner",
            "password": new_pass
        })
        
        # If this fails, the 'Integrity' between Reset and Login is broken.
        self.assertEqual(login_res.status_code, 200)
        self.assertIn('access', login_res.data)
        print("--- Integrity Test Passed: Full Recovery Flow Verified ---")