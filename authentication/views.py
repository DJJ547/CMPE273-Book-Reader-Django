from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2
from rest_framework import status
import requests
import json
import os
from dotenv import load_dotenv
load_dotenv()

@api_view(['POST'])
def app_signup(request):
    return

@api_view(['POST'])
def app_login(request):
    return

@api_view(['POST'])
def exchange_code(request):
    # Get the authorization code from the frontend
    data = json.loads(request.body)
    authorization_code = data.get('code')
    
    if not authorization_code:
        return Response({'error': 'Authorization code is missing'}, status=400)
    # Exchange the authorization code for access and refresh tokens
    token_data = {
        'code': authorization_code,
        'client_id': os.getenv('GOOGLE_OAUTH2_CLIENT_ID'),
        'client_secret': os.getenv('GOOGLE_OAUTH2_CLIENT_SECRET'),
        'redirect_uri': "postmessage",
        'grant_type': 'authorization_code',
    }
    print(token_data)

    token_response = requests.post(os.getenv('GOOGLE_TOKEN_URL'), data=token_data)
    print(token_response.status_code)
    print(token_response.json())

    if token_response.status_code != 200:
        return Response({'error': 'Failed to exchange code for tokens'}, status=token_response.status_code)

    token_response_data = token_response.json()

    # Extract access token and ID token (JWT containing user info)
    access_token = token_response_data.get('access_token')
    id_token = token_response_data.get('id_token')

    return Response({
        'access_token': access_token,
        'id_token': id_token,
    })

    