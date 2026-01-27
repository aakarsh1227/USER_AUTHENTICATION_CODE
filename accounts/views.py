from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator

# REST Framework Imports
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

# JWT & Local Imports
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, UserSerializer

# --- PAGE RENDERING ---
def login_page(request):
    """Renders the login.html template"""
    return render(request, 'login.html')

def home_view(request):
    """Renders the main dashboard/index template"""
    return render(request, 'accounts/index.html')

# --- FLOW 1: ONBOARDING & AUTHENTICATION ---

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # We add a clear "message" key here
            return Response({
                "message": "Registration Successful! You can now login.",
                "user": serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserProfileView(APIView):
    """Fetches user details using the Access Token."""
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
        
class LogoutView(APIView):
    """Blacklists the refresh token for security integrity."""
    permission_classes = [IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"message": "Logout Successful"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response({"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)

# --- FLOW 2: LOGGED-IN ACCOUNT MANAGEMENT (Inside App) ---

class UpdatePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Match the key 'new_password' from your script
        new_password = request.data.get("new_password") 
        
        if not new_password:
            return Response({"error": "New password is required"}, status=400)
        
        user = request.user
        user.set_password(new_password) # The secure hashing wrapper
        user.save()
        return Response({"message": "Password Updated Successfully!"}, status=status.HTTP_200_OK)
# --- FLOW 3: ACCOUNT RECOVERY (Forgot Password - Outside App) ---

class ForgetPasswordView(APIView):
    """Step 1: Generates a temporary security token via Email lookup."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            return Response({"token": token, "uid": uid, "message": "Recovery token generated."}, status=200)
        except User.DoesNotExist:
            return Response({"error": "Email not found"}, status=404)

class ResetPasswordConfirmView(APIView):
    """Step 2: Uses the uid and token to securely reset the password."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        uidb64 = request.data.get('uid')
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
            if default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully!"}, status=200)
            return Response({"error": "Invalid or expired token"}, status=400)
        except Exception:
            return Response({"error": "Invalid request"}, status=400)