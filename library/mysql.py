from mysql_models.models import Book, BookGenre, BookReview, BookProgress, Shelf, ShelfBook, WishlistBook


def fetch_shelves_data(user_id):
    try:
        library_data_map = {}
        shelves = Shelf.objects.filter(user_id=user_id)
        for shelf in shelves:
            library_data_map[shelf.name] = {
                "id": shelf.id,
                "name": shelf.name,
                "icon": shelf.icon,
                "background_color": shelf.background_color,
                "created_at": shelf.created_at,
                "updated_at": shelf.updated_at,
            }
            shelf_books_data = []
            shelf_books = ShelfBook.objects.filter(shelf_id=shelf.id)
            for shelf_book in shelf_books:
                shelf_book_data = fetch_book_meta(
                    user_id, shelf.id, shelf_book.book_id)
                shelf_books_data.append(shelf_book_data)
            library_data_map[shelf.name]['books'] = shelf_books_data
        return {"data": library_data_map, "message": f"Library data for user with id '{user_id}' successfully fetched."}
    except Exception as e:
        return {"data": {}, "message": f"An error occurred: {e}."}


def fetch_book_meta(user_id, shelf_id, book_id):
    try:
        book_meta = Book.objects.get(id=book_id)
        shelf_status = fetch_shelf_stat(shelf_id, book_id)
        wishlist_status = fetch_wishlist_stat(user_id, book_id)
        shelf_book_data = {
            "book_id": book_id,
            "book_name": book_meta.book_name,
            "author": book_meta.author,
            "book_link": book_meta.book_link,
            "book_cover": book_meta.book_cover,
            "book_description": book_meta.book_description,
            "num_of_chapters": book_meta.num_of_chapters,
            "shelf_added_at": shelf_status['added_at'],
            "is_wishlisted": wishlist_status['is_wishlisted'],
            "wishlist_added_at": wishlist_status['added_at'],
            "genres": fetch_book_genres(book_id),
            "average_rating": fetch_book_rating(book_id),
        }
        return shelf_book_data
    except Exception as e:
        print("An error occurred:", e)
        return []


def fetch_shelf_stat(shelf_id, book_id):
    try:
        shelf_stat = ShelfBook.objects.get(shelf_id=shelf_id, book_id=book_id)
        shelf_stat_data = {
            "added_at": shelf_stat.added_at,
        }
        return shelf_stat_data
    except Exception as e:
        print("An error occurred:", e)
        return []


def fetch_wishlist_stat(user_id, book_id):
    try:
        is_wishlisted = WishlistBook.objects.filter(
            user_id=user_id, book_id=book_id).exists()
        if is_wishlisted:
            wishlist_book = WishlistBook.objects.get(
                user_id=user_id, book_id=book_id)
            shelf_stat_data = {
                "is_wishlisted": is_wishlisted,
                "added_at": wishlist_book.added_at,
            }
        else:
            shelf_stat_data = {
                "is_wishlisted": is_wishlisted,
                "added_at": None,
            }
        return shelf_stat_data
    except Exception as e:
        print("An error occurred:", e)
        return []


def fetch_book_genres(book_id):
    try:
        book_genres = BookGenre.objects.filter(book_id=book_id)
        # Optionally, convert to a list of dictionaries or another format
        book_genres_data = [gen.genre for gen in book_genres]
        return book_genres_data
    except Exception as e:
        print("An error occurred:", e)
        return []


def fetch_book_rating(book_id):
    try:
        if BookReview.objects.filter(book_id=book_id).exists():
            book_reviews = BookReview.objects.filter(book_id=book_id)
            total_rating = 0
            for book_review in book_reviews:
                total_rating += book_review.rating
            return round(float(total_rating / len(book_reviews)), 2)
        else:
            return 0.0
    except Exception as e:
        print("An error occurred:", e)
        return 0.0


def fetch_wishlist_data(user_id):
    try:
        wishlist_books_data = []
        wishlist_books = WishlistBook.objects.filter(user_id=user_id)
        for wishlist_book in wishlist_books:
            book_meta = Book.objects.get(id=wishlist_book.book.id)
            wishlist_book_data = {
                "book_id": book_meta.id,
                "book_name": book_meta.book_name,
                "author": book_meta.author,
                "book_link": book_meta.book_link,
                "book_cover": book_meta.book_cover,
                "book_description": book_meta.book_description,
                "num_of_chapters": book_meta.num_of_chapters,
                "added_at": wishlist_book.added_at,
                "genres": fetch_book_genres(book_meta.id),
                "average_rating": fetch_book_rating(book_meta.id),
            }
            wishlist_books_data.append(wishlist_book_data)
        return {"data": wishlist_books_data, "message": f"Wishlist data for user with id '{user_id}' successfully fetched."}
    except Exception as e:
        return {"data": [], "message": f"An error occurred: {e}."}
    
    
def fetch_history_data(user_id):
    try:
        history_books_data = []
        history_books = BookProgress.objects.filter(user_id=user_id)
        for history_book in history_books:
            book_meta = Book.objects.get(id=history_book.book.id)
            history_book_data = {
                "book_id": book_meta.id,
                "book_name": book_meta.book_name,
                "author": book_meta.author,
                "book_link": book_meta.book_link,
                "book_cover": book_meta.book_cover,
                "book_description": book_meta.book_description,
                "num_of_chapters": book_meta.num_of_chapters,
                "last_read_at": history_book.last_read_at,
                "genres": fetch_book_genres(book_meta.id),
                "average_rating": fetch_book_rating(book_meta.id),
            }
            history_books_data.append(history_book_data)
        return {"data": history_books_data, "message": f"History data for user with id '{user_id}' successfully fetched."}
    except Exception as e:
        return {"data": [], "message": f"An error occurred: {e}."}


def fetch_shelves_list_data(user_id):
    try:
        shelves_data = []
        shelves = Shelf.objects.filter(user_id=user_id)
        for shelf in shelves:
            shelf_data = {
                "shelf_id": shelf.id,
                "shelf_name": shelf.name,
            }
            shelves_data.append(shelf_data)
        return {"data": shelves_data, "message": f"Shelves list data for user with id '{user_id}' successfully fetched."}
    except Exception as e:
        return {"data": [], "message": f"An error occurred: {e}."}


def add_shelf(user_id, shelf):
    try:
        if Shelf.objects.filter(user_id=user_id, name=shelf['name']).exists():
            return {"data": False, "message": f"A shelf with the name '{shelf['name']}' from user with id '{user_id}' already exists."}
        else:
            new_shelf = Shelf.objects.create(
                user_id=user_id,
                name=shelf['name'],
                icon=shelf['icon'],
                background_color=shelf['background_color']
            )
            new_shelf.save()
            return {"data": True, "message": "Shelf successfully created!"}
    except Exception as e:
        return {"data": False, "message": f"Error creating shelf: {e}"}


def remove_shelf(shelf_id):
    try:
        if not Shelf.objects.filter(id=shelf_id).exists():
            return {"data": False, "message": f"Shelf with given id '{shelf_id}' does not exist."}
        else:
            shelf = Shelf.objects.get(id=shelf_id)
            shelf.delete()
            return {"data": True, "message": f"Shelf with given id '{shelf_id}' successfully created!"}
    except Exception as e:
        return {"data": False, "message": f"Error creating shelf: {e}"}


def add_book_to_shelf(user_id, shelf_id, book_id):
    try:
        if ShelfBook.objects.filter(shelf__user_id=user_id, shelf_id=shelf_id, book_id=book_id).exists():
            return {"data": False, "message": f"A book with the book id '{book_id}' from user with id '{user_id}' already exists in the shelf with id '{shelf_id}'."}
        else:
            new_book = ShelfBook.objects.create(
                shelf_id=shelf_id, book_id=book_id)
            new_book.save()
            return {"data": True, "message": f"Book with id '{book_id}' from user with id '{user_id}' successfully added to the shelf with id '{shelf_id}'."}
    except Exception as e:
        return {"data": False, "message": f"Error adding book to shelf: {e}"}


def remove_book_from_shelf(shelf_id, book_id):
    try:
        if not ShelfBook.objects.filter(shelf_id=shelf_id, book_id=book_id).exists():
            return {"data": False, "message": f"The book with id '{book_id}' does not exist in the shelf with id '{shelf_id}'."}
        else:
            shelf_book = ShelfBook.objects.get(
                shelf_id=shelf_id, book_id=book_id)
            shelf_book.delete()
            return {"data": True, "message": f"The book with id '{book_id}' successfully removed from the shelf with id '{shelf_id}'"}
    except Exception as e:
        return {"data": False, "message": f"Error removing book from shelf: {e}"}


def add_book_to_wishlist(user_id, book_id):
    try:
        if WishlistBook.objects.filter(user_id=user_id, book_id=book_id).exists():
            return {"data": False, "message": f"A book with the book id '{book_id}' from user with id '{user_id}' already exists in the wishlist."}
        else:
            new_withlist_book = WishlistBook.objects.create(
                user_id=user_id,
                book_id=book_id,
            )
            new_withlist_book.save()
            return {"data": True, "message": f"Book with id '{book_id}' from user with id '{user_id}' successfully added to the wishlist."}
    except Exception as e:
        return {"data": False, "message": f"Error adding book to wishlist: {e}"}


def remove_book_from_wishlist(user_id, book_id):
    try:
        if not WishlistBook.objects.filter(user_id=user_id, book_id=book_id).exists():
            return {"data": False, "message": f"The book with id '{book_id}' from user with id '{user_id}' does not exist in the wishlist."}
        else:
            withlist_book = WishlistBook.objects.get(
                user_id=user_id, book_id=book_id)
            withlist_book.delete()
            return {"data": True, "message": f"The book with id '{book_id}' from user with id '{user_id}' successfully removed from the wishlist."}
    except Exception as e:
        return {"data": False, "message": f"Error removing book from wishlist: {e}"}
