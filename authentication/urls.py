from django.urls import path
from .views import signup_view, login_view, exchange_code

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('exchange-code/', exchange_code, name='exchange_code'),
]