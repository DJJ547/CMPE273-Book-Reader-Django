import requests
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_BOOKS_APIS_KEY = os.getenv('GOOGLE_BOOKS_APIS_KEY')
GOOGLE_BOOKS_API_URL = os.getenv('GOOGLE_BOOKS_API_URL')

# Function to filter Gutendex results using Google Books API
def google_filter_results(gutendex_books):
    verified_books = []
    
    for book in gutendex_books:
        title = book.get("title")
        author = book.get("author")
        if not title or not author:
            continue  # Skip if title or authors are missing
        
        # Create search query for Google Books API with title and author
        google_books_query = f"{title} {author}"
        google_books_url = f"{GOOGLE_BOOKS_API_URL}?q={google_books_query}"
        
        try:
            google_response = requests.get(google_books_url, timeout=10)
            google_response.raise_for_status()
            google_data = google_response.json()
            
            # Check if any items were found in Google Books
            if google_data.get("totalItems", 0) > 0:
                book['gutendex_id'] = book.pop("id")
                book['google_id'] = google_data["items"][0]["id"]
                verified_books.append(book)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Google Books: {e}")
    
    return verified_books

# Function to filter Gutendex results using Google Books API
def google_filter_genre_results(gutendex_books):
    verified_books = []
    
    for book in gutendex_books:
        title = book.get("title")
        author = book.get("author")
        google_books_query = f"{title}" + " ".join(author)
        google_books_url = f"{GOOGLE_BOOKS_API_URL}?q={google_books_query}"
        
        try:
            google_response = requests.get(google_books_url, timeout=10)
            google_response.raise_for_status()
            google_data = google_response.json()
            
            # Check if any items were found in Google Books
            if google_data.get("totalItems", 0) > 0:
                book['gutendex_id'] = book.pop("id")
                book['google_id'] = google_data["items"][0]["id"]
                verified_books.append(book)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from Google Books: {e}")
    
    return verified_books

def google_fetch_books(query):
    # Limit the number of results to 10
    params = {'q': query, 'maxResults': 20, 'key': GOOGLE_BOOKS_APIS_KEY}
    
    try:
        response = requests.get(GOOGLE_BOOKS_API_URL, params=params, timeout=10)  # Added a timeout
        response.raise_for_status()  # Raises an HTTPError if the status is 4xx or 5xx
        
        books = response.json().get('items', [])
        book_list = []

        for book in books:
            volume_info = book.get('volumeInfo', {})
            book_data = {
                'id': book.get('id', ''),
                'title': volume_info.get('title', 'No Title'),
                'authors': volume_info.get('authors', []),
                # Placeholder if no thumbnail is available
                'thumbnail': volume_info.get('imageLinks', {}).get('thumbnail', 'https://via.placeholder.com/150'),
                'isbn': get_isbn(volume_info)  # Get ISBN if available
            }
            book_list.append(book_data)

        return book_list
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Google Books API: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error processing the response data: {e}")
    
    return []


def get_isbn(volume_info):
    identifiers = volume_info.get('industryIdentifiers', [])
    for identifier in identifiers:
        if identifier.get('type') == 'ISBN_13':
            return identifier.get('identifier')
    return None

# Google Books API that performs a book search and returns a list of books with fixed size (pagination)


def google_fetch_books_paginated(query, start_index=0, max_results=10):
    if query:
        url = (
            f'{GOOGLE_BOOKS_API_URL}?q={query}'
            f'&startIndex={start_index}&maxResults={max_results}&key={GOOGLE_BOOKS_APIS_KEY}'
        )
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None
    return None


def google_fetch_specific_books(genre, max_results=10):
    if genre:
        url = (
            f'{GOOGLE_BOOKS_API_URL}?q={genre}'
            f'&maxResults={max_results}&orderBy=relevance&key={GOOGLE_BOOKS_APIS_KEY}'
        )
        response = requests.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            return None
    return None


def google_fetch_book_reviews(book_title):
    if book_title:
        url = f'{GOOGLE_BOOKS_API_URL}?q={book_title}&key={GOOGLE_BOOKS_APIS_KEY}'
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
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
            return reviews
        else:
            return None
    return None
