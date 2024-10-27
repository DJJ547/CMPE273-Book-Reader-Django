import requests
import os
from dotenv import load_dotenv
load_dotenv()
GUTENDEX_API_URL = os.getenv('GUTENDEX_API_URL')
TIMEOUT = 20

# Define headers for requests
HEADERS = {
    "User-Agent": "MyBookApp/1.0 (http://localhost:3000/test; contact@example.com)",  # Use localhost for local dev
    "From": "contact@example.com",  # Provide an email in case they need to contact you
}
# Function to search for the book using Gutendex API
def gutendex_fetch_books(query, page=1, page_size=20):
    gutendex_url = f"{GUTENDEX_API_URL}?search={query}&page={page}&page_size={page_size}"
    try:
        response = requests.get(gutendex_url, headers=HEADERS, timeout=TIMEOUT)  # Set a timeout to avoid hanging
        response.raise_for_status()  # Will raise an HTTPError for bad responses
        gutendex_books = response.json().get('results', [])
        
        books_list = []
        for book in gutendex_books:
            download_url = book.get("formats", {}).get("text/plain; charset=utf-8")
            cover_url = book.get("formats", {}).get("image/jpeg")
            book_content_url = book.get("formats", {}).get("text/html")
            # Only include if both full content and a cover image are available
            if download_url and cover_url:
                book_info = {
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "author": ", ".join([author["name"] for author in book.get("authors", [])]),
                    "download_url": download_url,
                    "cover_url": cover_url,
                    "gutendex_url": f"https://www.gutenberg.org/ebooks/{book.get('id')}",
                    "content_url": book_content_url
                }
                books_list.append(book_info)
        return books_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Gutendex: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error processing the response data: {e}")
    
    return None


# Function to fetch full book content from Gutendex API
def gutendex_fetch_book_content(gutenberg_id):
    if not gutenberg_id:
        return None
    
    gutendex_url = f"{GUTENDEX_API_URL}?ids={gutenberg_id}"
    try:
        response = requests.get(gutendex_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        
        # Get book data
        book_data = response.json().get('results', [])[0]  # Assuming single result with the given ID
        
        # Find the URL for the plain text format
        text_url = book_data.get("formats", {}).get("text/plain; charset=utf-8")
        if not text_url:
            print("Full text content not available in 'text/plain; charset=utf-8' format.")
            return None
        
        # Download the book content
        text_response = requests.get(text_url, headers=HEADERS, timeout=TIMEOUT)
        text_response.raise_for_status()
        
        # Prepare filename
        filename = f"{book_data.get('title', 'book')}.txt"
        return text_response.text, filename
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Gutendex: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error processing the response data: {e}")
    
    return None


# Function to fetch books by genre keyword from Gutendex API
def gutendex_fetch_specific_books(genre, limit=10):
    if not genre:
        return None
    gutendex_url = f"{GUTENDEX_API_URL}?search={genre}&page_size={limit}"
    try:
        response = requests.get(gutendex_url, headers=HEADERS, timeout=TIMEOUT)
        response.raise_for_status()
        books_data = response.json().get('results', [])
        books_list = []
        for book in books_data:
            download_url = book.get("formats", {}).get("text/plain; charset=utf-8")
            book_content_url = book.get("formats", {}).get("text/html")
            if download_url:  # Only include if full content is available
                book_info = {
                    "id": book.get("id"),
                    "title": book.get("title"),
                    "author": ", ".join([author["name"] for author in book.get("authors", [])]),
                    "download_url": download_url,
                    "cover_url": book.get("formats", {}).get("image/jpeg"),
                    "gutendex_url": f"https://www.gutenberg.org/ebooks/{book.get('id')}",
                    "content_url": book_content_url
                }
                books_list.append(book_info)
        return books_list
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Gutendex: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error processing the response data: {e}")
    
    return None
    