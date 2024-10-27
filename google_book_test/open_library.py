import requests
import os
from dotenv import load_dotenv
load_dotenv()
OPEN_LIBRARY_API_URL = os.getenv('OPEN_LIBRARY_API_URL')

# Function to check if Open Library has the book content
def open_library_check_content_by_isbn(isbn):
    if not isbn:
        return False

    open_library_url = f"{OPEN_LIBRARY_API_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    # open_library_url =f"https://openlibrary.org/isbn/{isbn}.json"
    
    try:
        response = requests.get(open_library_url, timeout=10)  # Set a timeout to avoid hanging
        response.raise_for_status()  # Will raise an HTTPError for bad responses

        data = response.json()
        print(data)
        # Check if Open Library has the book content using the ISBN
        return True
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Open Library: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error processing the response data: {e}")
    
    return False


def open_library_fetch_book_content(isbn):
    if not isbn:
        return False
    open_library_url = f"{OPEN_LIBRARY_API_URL}?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
    
    try:
        response = requests.get(open_library_url, timeout=10)  # Set a timeout to avoid hanging
        response.raise_for_status()  # Will raise an HTTPError for bad responses

        data = response.json()
        
        # Check if the response contains data for the ISBN
        if f"ISBN:{isbn}" in data:
            book_data = data[f"ISBN:{isbn}"]
            
            # Check for the 'formats' field which might contain downloadable content
            if 'formats' in book_data:
                return book_data['formats']  # Return available formats for download
            
            return {"info": "No downloadable content available for this ISBN"}
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Open Library: {e}")
    except (KeyError, ValueError) as e:
        print(f"Error processing the response data: {e}")
    
    return None
