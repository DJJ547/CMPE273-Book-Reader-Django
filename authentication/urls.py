from django.urls import path
from .views import exchange_code, app_signup, app_login

urlpatterns = [
    path('signup/', app_signup, name='signup'),
    path('login/', app_login, name='login'),
    path('exchange-code/', exchange_code, name='exchange_code'),
]