from django.urls import path, include
from .views import RegisterUser, GoogleLogin

urlpatterns = [
    path('signup/', RegisterUser.as_view(), name="register_signup"),
    path('login/', GoogleLogin.as_view(), name="google_login"),
#    path('admin/', admin.site.urls),
]
