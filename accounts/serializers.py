from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    """Used to send user data back to the client (JSON)"""
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class RegisterSerializer(serializers.ModelSerializer):
    """Used for Onboarding (Registration)"""
    # Professional Tip: Ensure email is required so Forget Password works later!
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8} # Security: Write-only + Length check
        }

    def create(self, validated_data):
        # The create_user wrapper handles password hashing automatically
        user = User.objects.create_user(**validated_data)
        return user
    
class ResetPasswordSerializer(serializers.Serializer):
    """Used for Section 2: Update Password (Logged-in users)"""
    new_password = serializers.CharField(
        write_only=True, 
        min_length=8, 
        style={'input_type': 'password'}
    )
    
    # You can add a 'confirm_password' field here later for extra integrity!