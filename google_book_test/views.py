import requests
import os
from django.conf import settings
from rest_framework.response import Response
from dotenv import load_dotenv
from rest_framework.decorators import api_view
from django.conf import settings
import json


load_dotenv()
api_key = os.getenv('GOOGLE_BOOKS_APIS_KEY')
GOOGLE_BOOKS_API_URL = "https://www.googleapis.com/books/v1/volumes"

# Google Books API that performs a book search and returns a list of books
@api_view(['GET'])
def get_books(request):
    query = request.GET.get('q')
    if query:
        # Assuming the Google Books API key is stored in Django settings
        url = f'{GOOGLE_BOOKS_API_URL}?q={query}&key={api_key}'
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response({'error': 'Failed to fetch books from Google Books API'}, status=500)
    else:
        return Response({'error': 'No query provided'}, status=400)

# Google Books API that performs a book search and returns a list of books with fixed size (pagination)
@api_view(['GET'])
def get_books_paginated(request):
    query = request.GET.get('q')
    start_index = request.GET.get('startIndex', 0)  # Default to 0 if not provided
    max_results = request.GET.get('maxResults', 10)  # Default to 10 results per page

    if query:
        url = (
            f'{GOOGLE_BOOKS_API_URL}?q={query}'
            f'&startIndex={start_index}&maxResults={max_results}&key={api_key}'
        )
        
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return Response(data)
        else:
            return Response({'error': 'Failed to fetch books from Google Books API'}, status=500)
    else:
        return Response({'error': 'No query provided'}, status=400)

@api_view(['GET'])
def get_specific_books(request):
    # Use a query that typically returns popular or top-rated books
    genre = request.GET.get('genre')
    max_results = int(request.query_params.get('maxResults', 10))  # Default to 10 results

    url = (
        f'{GOOGLE_BOOKS_API_URL}?q={genre}'
        f'&maxResults={max_results}&orderBy=relevance&key={api_key}'
    )
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return Response(data)
    else:
        return Response({'error': 'Failed to fetch books from Google Books API'}, status=500)

@api_view(['GET'])
def get_book_reviews(request):
    book_title = request.GET.get('title')
    if not book_title:
        return Response({'error': 'Title is required'}, status=400)
    url = f'https://www.googleapis.com/books/v1/volumes?q={book_title}&key={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        # Extracting the relevant information
        reviews = []
        for item in data.get('items', []):
            volume_info = item.get('volumeInfo', {})
            reviews.append({
                'title': volume_info.get('title'),
                'authors': volume_info.get('authors'),
                'description': volume_info.get('description'),
                'average_rating': volume_info.get('averageRating'),
                'ratings_count': volume_info.get('ratingsCount')
            })
        return Response({'reviews': reviews})
    else:
        return Response({'error': 'Failed to fetch reviews'}, status=500)
    
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
        'redirect_uri': 'postmessage',
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
    
@api_view(['POST'])
def get_google_books_reading_list(request):
    data = json.loads(request.body)
    access_token = data.get('access_token')

    if not access_token:
        return Response({'error': 'Access token is missing'}, status=400)

    # Make a request to the Google Books API to get the user's reading list
    headers = {
        'Authorization': f'Bearer {access_token}',
    }

    books_response = requests.get(settings.GOOGLE_BOOKS_API_URL, headers=headers)

    if books_response.status_code != 200:
        return Response({'error': 'Failed to retrieve reading list'}, status=books_response.status_code)

    books_data = books_response.json()

    return Response(books_data)


