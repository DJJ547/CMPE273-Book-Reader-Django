"""
URL configuration for book_reader_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('ai/', include('ai_lambda.urls')),
    path('auth/', include('authentication.urls')),
    path('main/', include('main_search_single.urls')),
    path('listhistory/', include('list_history.urls')),
    path('reading/', include('reading_page.urls')),
    path('accounts/', include('allauth.urls')),  # Allauth URLs for social login

    # This will route all the OAuth-related URLs to the social_django views, including the complete/google/ endpoint for handling OAuth responses.
    path('oauth/', include('social_django.urls', namespace='social')),
    path('api/', include('google_book_test.urls')),
]
