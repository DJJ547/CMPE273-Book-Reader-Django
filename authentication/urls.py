from django.urls import path, include
from .views import BuiltInRegister, GoogleLogin, BuiltInLogin

urlpatterns = [
    path('signup/', BuiltInRegister.as_view(), name="register signup"),
    path('login/', BuiltInLogin.as_view(), name="built-in login"),
    path('google_login/', GoogleLogin.as_view(), name="google login"),
#    path('admin/', admin.site.urls),
]
