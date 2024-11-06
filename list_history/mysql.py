from mysql_models.models import Book, ReadingLists, ReadingListBook, BookGenre

def fetch_reading_list_books(reading_list_id):
    list_books = ReadingListBook.objects.filter(id=reading_list_id)
    for book in list_books:
        book_meta = Book.objects.filter(id=book.book_id)
        book_data = {
            "book_id": book.book_id,
            
            "added_at": book.added_at,
            "status": book.status,
        }
    list_books_data = []
    list_books_data.append(book_data)
    return []

# Fetch all reading lists associated with a specific user_id.
def fetch_reading_lists_with_books(user_id):
    try:
        reading_lists = ReadingLists.objects.filter(user_id=user_id)
        # Optionally, convert to a list of dictionaries or another format
        reading_list_data = [
            {
                "id": rl.id,
                "user_id": rl.user_id,
                "name": rl.name,
                "description": rl.description,
                "created_at": rl.created_at,
                "updated_at": rl.updated_at,
                "flag_color": rl.flag_color,
                "books": fetch_reading_list_books(rl.id),
            }
            for rl in reading_lists
        ]
        return reading_list_data
    except Exception as e:
        print("An error occurred:", e)
        return []
    
def fetch_book_genres(book_id):
    try:
        book_genres = BookGenre.objects.filter(book=book_id)
        # Optionally, convert to a list of dictionaries or another format
        book_genres_data = [
            {
                "book_id": gen.book_id,
                "genre": gen.genre,
            }
            for gen in book_genres
        ]
        return book_genres_data
    except Exception as e:
        print("An error occurred:", e)
        return []
    