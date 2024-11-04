from django.urls import path, include
from .views import RegisterUser, GoogleLogin

urlpatterns = [
    path('register/', RegisterUser.as_view(), name="register_user"),
    path('google-login/', GoogleLogin.as_view(), name="google_login"),
#    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),  
]
