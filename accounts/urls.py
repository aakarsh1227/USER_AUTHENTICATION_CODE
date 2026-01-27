from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    RegisterView, 
    LogoutView, 
    UpdatePasswordView, 
    ForgetPasswordView, 
    ResetPasswordConfirmView, 
    UserProfileView, 
    home_view,
    login_page
)

# accounts/urls.py

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', RegisterView.as_view(), name='register'),
    
    # 1. Ensure this is exactly 'login/' to match your JS 'API + login/'
    path('login/', TokenObtainPairView.as_view(), name='login'), 
    
    # 2. These match the Section 1: Recovery logic
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-confirm/', ResetPasswordConfirmView.as_view(), name='reset_confirm'),
    
    # 3. This matches the Section 2: Authenticated logic
    path('update-password/', UpdatePasswordView.as_view(), name='update_password'),
    
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]