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

# accounts/urls.py   (routers for accounts app)

urlpatterns = [
    path('', home_view, name='home'),   # Renders the main dashboard/index template
    path('register/', RegisterView.as_view(), name='register'),   # User Registration Endpoint
    
    # login page rendering
    path('login/', TokenObtainPairView.as_view(), name='login'), #token get endpoint
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    
    # User profile endpoint
    path('forget-password/', ForgetPasswordView.as_view(), name='forget_password'),
    path('reset-confirm/', ResetPasswordConfirmView.as_view(), name='reset_confirm'),
    
    # under login user management
    path('update-password/', UpdatePasswordView.as_view(), name='update_password'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]