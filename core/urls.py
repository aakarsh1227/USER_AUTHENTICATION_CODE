from django.contrib import admin
from django.urls import path, include
from accounts.views import home_view # Import only the home view for the root path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # This is the most important line. 
    # It tells Django: "For anything starting with accounts/, look inside accounts/urls.py"
    path('accounts/', include('accounts.urls')), 

    # This handles the base URL: http://127.0.0.1:8000/
    path('', home_view, name='home'), 
]