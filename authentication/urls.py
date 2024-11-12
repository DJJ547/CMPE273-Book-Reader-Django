from django.urls import path, include
from .views import RegisterUser, GoogleLogin

urlpatterns = [
    path('signup/', RegisterUser.as_view(), name="signup"),
    path('login/', GoogleLogin.as_view(), name="login"),
#    path('admin/', admin.site.urls),
]
