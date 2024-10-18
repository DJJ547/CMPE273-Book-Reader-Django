from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
from social_django.utils import load_strategy
from social_core.backends.google import GoogleOAuth2
from rest_framework import status
from django.contrib.auth.decorators import login_required
import requests

# Custom JWT Token Creation
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

# Signup View (Function-Based)
@api_view(['POST'])
def signup_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'User already exists'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password)
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

# Traditional Login View (Function-Based)
@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        tokens = get_tokens_for_user(user)
        return Response(tokens, status=status.HTTP_200_OK)
    
    return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

# # Google Login View (Function-Based)
# @api_view(['POST'])
# def google_login(request):
#     token = request.data.get('token')
#     if not token:
#         return Response({'error': 'Token is required'}, status=400)
    
#     strategy = load_strategy(request)
#     backend = GoogleOAuth2(strategy=strategy)
#     user = backend.do_auth(token)

#     if user:
#         tokens = get_tokens_for_user(user)
#         return Response(tokens)
    
#     return Response({'error': 'Login failed'}, status=400)

@api_view(['POST'])
def google_login(request):
    token = request.data.get('token')
    if not token:
        return Response({'error': 'Token is required'}, status=400)
    
    strategy = load_strategy(request)
    backend = GoogleOAuth2(strategy=strategy)
    user = backend.do_auth(token)

    if user:
        # Extract the access token and refresh token
        social = user.social_auth.get(provider='google-oauth2')
        access_token = social.extra_data['access_token']
        refresh_token = social.extra_data.get('refresh_token')

        # Save or update tokens for future use if necessary
        # You can store this in session, DB, or cache depending on your use case

        # Optional: Generate JWT tokens if you're using JWT for session handling
        tokens = get_tokens_for_user(user)

        return Response({
            'tokens': tokens,  # JWT tokens for authentication if you're using them
            'google_access_token': access_token,
            'google_refresh_token': refresh_token
        })
    
    return Response({'error': 'Login failed'}, status=400)

@login_required
def get_bookshelves(request):
    user = request.user

    # Get user's social auth token
    social = user.social_auth.get(provider='google-oauth2')
    access_token = social.extra_data['access_token']

    # Make a request to Google Books API to get user's bookshelves
    response = requests.get(
        'https://www.googleapis.com/books/v1/mylibrary/bookshelves',
        headers={'Authorization': f'Bearer {access_token}'}
    )

    if response.status_code == 200:
        return Response(response.json())
    else:
        return Response({'error': 'Failed to fetch bookshelves'}, status=response.status_code)
    