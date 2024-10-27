import requests
import os
from dotenv import load_dotenv
load_dotenv()
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework import status
import json

from .google_books import google_filter_results, google_fetch_book_reviews, google_filter_genre_results
# from .open_library import open_library_check_content_by_isbn, open_library_fetch_book_content
from .gutendex import gutendex_fetch_books, gutendex_fetch_book_content, gutendex_fetch_specific_books

@api_view(['GET'])
def search_books(request):
    query = request.GET.get('q', '')
    page = request.GET.get('page', '')
    page_size = request.GET.get('page_size', '')
    if not query:
        return Response({'books': []})
    gutendex_books_results = gutendex_fetch_books(query, page, page_size)
    print(gutendex_books_results)
    if not gutendex_books_results:
        return Response({'books': []})
    filtered_results = google_filter_results(gutendex_books_results)
    return Response({'books': filtered_results})

@api_view(['GET'])
def fetch_book_content(request):
    gutenberg_id = request.GET.get('id', '')
    # Fetch the book content and filename
    result = gutendex_fetch_book_content(gutenberg_id)
    if not result:
        return Response({"detail": "Full text content not available for this book."}, status=status.HTTP_404_NOT_FOUND)
    
    book_content, filename = result  # Safe to unpack now
    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }
    return Response(
        book_content,
        headers=headers,
        content_type='text/plain',
        status=status.HTTP_200_OK
    )
    

@api_view(['GET'])
def get_books_by_genre(request):
    genre = request.GET.get('genre')
    max_results = int(request.query_params.get('maxResults', 10))  # Default to 10 results

    if genre:
        book_results = gutendex_fetch_specific_books(genre, max_results)
        if not book_results:
            return Response([])
        filtered_results = google_filter_genre_results(book_results)
        return Response(filtered_results)
    else:
        return Response({'error': 'No genre provided'}, status=400)


@api_view(['GET'])
def get_book_reviews(request):
    book_title = request.GET.get('title')
    if not book_title:
        return Response({'error': 'Title is required'}, status=400)

    reviews = google_fetch_book_reviews(book_title)
    if reviews is not None:
        return Response({'reviews': reviews})
    else:
        return Response({'error': 'Failed to fetch reviews'}, status=500)
    
    
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

    books_response = requests.get(os.getenv('GOOGLE_BOOKS_API_URL'), headers=headers)

    if books_response.status_code != 200:
        return Response({'error': 'Failed to retrieve reading list'}, status=books_response.status_code)

    books_data = books_response.json()

    return Response(books_data)

