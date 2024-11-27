from mysql_models.models import Book, BookGenre, BookReview, BookProgress, Shelf, ShelfBook, WishlistBook


def fetch_library_data(user_id):
    library_data_map = {}
    try:
        shelves_data_list = []
        shelves = Shelf.objects.filter(user_id=user_id)
        for shelf in shelves:
            shelf_data = {
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
            shelf_data['books'] = shelf_books_data
            shelves_data_list.append(shelf_data)
        library_data_map["Shelves"] = shelves_data_list

        wishlist_books_data = []
        wishlist_books = WishlistBook.objects.filter(user_id=user_id)
        for wishlist_book in wishlist_books:
            book_meta = Book.objects.get(id=wishlist_book.book.id)
            history_status = fetch_history_stat(user_id, wishlist_book.book.id)
            wishlist_book_data = {
                "book_id": book_meta.id,
                "book_name": book_meta.book_name,
                "author": book_meta.author,
                "book_link": book_meta.book_link,
                "book_cover": book_meta.book_cover,
                "book_description": book_meta.book_description,
                "num_of_chapters": book_meta.num_of_chapters,
                "current_chapter": history_status['current_chapter'],
                "last_read_at": history_status['last_read_at'],
                "is_wishlisted": True,
                "wishlist_added_at": wishlist_book.added_at,
                "genres": fetch_book_genres(book_meta.id),
                "average_rating": fetch_book_rating(book_meta.id),
            }
            wishlist_books_data.append(wishlist_book_data)
        library_data_map["Wishlist"] = wishlist_books_data

        history_books_data = []
        history_books = BookProgress.objects.filter(user_id=user_id)
        for history_book in history_books:
            book_meta = Book.objects.get(id=history_book.book.id)
            wishlist_status = fetch_wishlist_stat(
                user_id, history_book.book.id)
            history_book_data = {
                "book_id": book_meta.id,
                "book_name": book_meta.book_name,
                "author": book_meta.author,
                "book_link": book_meta.book_link,
                "book_cover": book_meta.book_cover,
                "book_description": book_meta.book_description,
                "num_of_chapters": book_meta.num_of_chapters,
                "is_wishlisted": wishlist_status['is_wishlisted'],
                "wishlist_added_at": wishlist_status['wishlist_added_at'],
                "current_chapter": history_book.current_chapter,
                "last_read_at": history_book.last_read_at,
                "genres": fetch_book_genres(book_meta.id),
                "average_rating": fetch_book_rating(book_meta.id),
            }
            history_books_data.append(history_book_data)
        library_data_map["History"] = history_books_data

        return {"data": library_data_map, "message": f"Library data for user with id '{user_id}' successfully fetched."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"data": {}, "message": f"An error occurred: {e}."}


def fetch_shelves_data(user_id):
    try:
        shelves_data_map = {}
        shelves = Shelf.objects.filter(user_id=user_id)
        for shelf in shelves:
            shelves_data_map[shelf.name] = {
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
            shelves_data_map[shelf.name]['books'] = shelf_books_data
        return {"data": shelves_data_map, "message": f"Shelves data for user with id '{user_id}' successfully fetched."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"data": {}, "message": f"An error occurred: {e}."}


def fetch_shelves_with_current_book(user_id, book_id):
    try:
        shelves_data_list = []
        shelves = Shelf.objects.filter(user_id=user_id)
        for shelf in shelves:
            book_is_in_shelf = False
            shelf_obj = {
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
                if shelf_book.book_id == book_id:
                    book_is_in_shelf = True
                shelf_book_data = fetch_book_meta(
                    user_id, shelf.id, shelf_book.book_id)
                shelf_books_data.append(shelf_book_data)
            shelf_obj['books'] = shelf_books_data
            if book_is_in_shelf:
                shelves_data_list.append(shelf_obj)
        return {"result": True if shelves_data_list else False, "data": shelves_data_list, "message": f"Shelves data list for user with id '{user_id}' for book with id '{book_id}' successfully fetched."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "data": [], "message": f"An error occurred: {e}."}


def fetch_shelves_without_current_book(user_id, book_id):
    try:
        shelves_data_without_book = []
        shelves = Shelf.objects.filter(user_id=user_id)
        for shelf in shelves:
            book_is_in_shelf = False
            shelf_obj = {
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
                if shelf_book.book_id == book_id:
                    book_is_in_shelf = True
                shelf_book_data = fetch_book_meta(
                    user_id, shelf.id, shelf_book.book_id)
                shelf_books_data.append(shelf_book_data)
            shelf_obj['books'] = shelf_books_data
            if not book_is_in_shelf:
                shelves_data_without_book.append(shelf_obj)
        return {"result": True if shelves_data_without_book else False, "data": shelves_data_without_book, "message": f"Shelves data list for user with id '{user_id}' for book with id '{book_id}' successfully fetched."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "data": [], "message": f"An error occurred: {e}."}


def fetch_book_meta(user_id, shelf_id, book_id):
    try:
        book_meta = Book.objects.get(id=book_id)
        shelf_status = fetch_shelf_stat(shelf_id, book_id)
        wishlist_status = fetch_wishlist_stat(user_id, book_id)
        history_status = fetch_history_stat(user_id, book_id)
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
            "wishlist_added_at": wishlist_status['wishlist_added_at'],
            "current_chapter": history_status['current_chapter'],
            "last_read_at": history_status['last_read_at'],
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


def fetch_history_stat(user_id, book_id):
    try:
        is_in_history = BookProgress.objects.filter(
            user_id=user_id, book_id=book_id).exists()
        if is_in_history:
            history_book = BookProgress.objects.get(
                user_id=user_id, book_id=book_id)
            shelf_stat_data = {
                "current_chapter": history_book.current_chapter,
                "last_read_at": history_book.last_read_at,
            }
        else:
            shelf_stat_data = {
                "current_chapter": 0,
                "last_read_at": None,
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
                "wishlist_added_at": wishlist_book.added_at,
            }
        else:
            shelf_stat_data = {
                "is_wishlisted": is_wishlisted,
                "wishlist_added_at": None,
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
        print(f"Exception: {e}")
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
        print(f"Exception: {e}")
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
        print(f"Exception: {e}")
        return {"data": [], "message": f"An error occurred: {e}."}


def add_shelf(user_id, shelf):
    try:
        added_shelf_data = {}
        if Shelf.objects.filter(user_id=user_id, name=shelf['name']).exists():
            return {"result": False, "data": added_shelf_data, "message": f"A shelf with the name '{shelf['name']}' from user with id '{user_id}' already exists."}
        else:
            new_shelf = Shelf.objects.create(
                user_id=user_id,
                name=shelf['name'],
                icon=shelf['icon'],
                background_color=shelf['background_color']
            )
            new_shelf.save()
            added_shelf = Shelf.objects.get(
                user_id=user_id, name=shelf['name'])
            added_shelf_data = {
                "id": added_shelf.id,
                "name": added_shelf.name,
                "icon": added_shelf.icon,
                "background_color": added_shelf.background_color,
                "created_at": added_shelf.created_at,
                "updated_at": added_shelf.updated_at,
                "books": []
            }
            return {"result": True, "data": added_shelf_data, "message": "Shelf successfully created!"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "data": added_shelf_data, "message": f"Error creating shelf: {e}"}


def edit_shelf(user_id, shelf):
    try:
        if not Shelf.objects.filter(user_id=user_id, id=shelf['id']).exists():
            return {"result": False, "data": {}, "message": f"A shelf with the id '{shelf['id']}' from user with id '{user_id}' does not exists."}
        shelf_to_edit = Shelf.objects.get(user_id=user_id, id=shelf['id'])
        shelf_to_edit.name = shelf['name']
        shelf_to_edit.icon = shelf['icon']
        shelf_to_edit.background_color = shelf['background_color']
        shelf_to_edit.save()
        edited_shelf = Shelf.objects.get(user_id=user_id, id=shelf['id'])
        edited_shelf_data = {
            "id": edited_shelf.id,
            "name": edited_shelf.name,
            "icon": edited_shelf.icon,
            "background_color": edited_shelf.background_color,
            "created_at": edited_shelf.created_at,
            "updated_at": edited_shelf.updated_at,
            "books": []
        }
        shelf_books_data = []
        shelf_books = ShelfBook.objects.filter(shelf_id=shelf['id'])
        for shelf_book in shelf_books:
            shelf_book_data = fetch_book_meta(
                user_id, shelf['id'], shelf_book.book_id)
            shelf_books_data.append(shelf_book_data)
        edited_shelf_data['books'] = shelf_books_data
        return {"result": True, "data": edited_shelf_data, "message": "Shelf successfully edited!"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "message": f"Error editing shelf: {e}"}


def remove_shelf(user_id, shelf_id):
    try:
        if not Shelf.objects.filter(user_id=user_id, id=shelf_id).exists():
            return {"result": False, "message": f"Shelf with given id '{shelf_id}' does not exist."}
        else:
            shelf = Shelf.objects.get(id=shelf_id)
            shelf.delete()
            return {"result": True, "message": f"Shelf with given id '{shelf_id}' successfully removed!"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "message": f"Error creating shelf: {e}"}


def add_book_to_shelf(user_id, shelf_id, book_id):
    try:
        if ShelfBook.objects.filter(shelf_id=shelf_id, book_id=book_id).exists():
            print(f"A book with the book id '{book_id}' from user with id '{user_id}' already exists in the shelf with id '{shelf_id}'.")
            return {"result": False, "data": {}, "message": f"A book with the book id '{book_id}' from user with id '{user_id}' already exists in the shelf with id '{shelf_id}'."}
        else:
            new_book = ShelfBook.objects.create(
                shelf_id=shelf_id, book_id=book_id)
            new_book.save()
            added_book = fetch_book_meta(user_id, shelf_id, book_id)
            print(f"Book with id '{book_id}' from user with id '{user_id}' successfully added to the shelf with id '{shelf_id}'.")
            return {"result": True, "data": added_book, "message": f"Book with id '{book_id}' from user with id '{user_id}' successfully added to the shelf with id '{shelf_id}'."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "data": {}, "message": f"Error adding book to shelf: {e}"}


def remove_book_from_shelf(user_id, shelf_id, book_id):
    try:
        if not ShelfBook.objects.filter(shelf_id=shelf_id, book_id=book_id).exists():
            print(f"The book with id '{book_id}' does not exist in the shelf with id '{shelf_id}'.")
            return {"result": False, "message": f"The book with id '{book_id}' does not exist in the shelf with id '{shelf_id}'."}
        else:
            shelf_book = ShelfBook.objects.get(
                shelf_id=shelf_id, book_id=book_id)
            shelf_book.delete()
            print(f"The book with id '{book_id}' successfully removed from the shelf with id '{shelf_id}'")
            return {"result": True, "message": f"The book with id '{book_id}' successfully removed from the shelf with id '{shelf_id}'"}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "message": f"Error removing book from shelf: {e}"}


def add_book_to_wishlist(user_id, book_id):
    try:
        if WishlistBook.objects.filter(user_id=user_id, book_id=book_id).exists():
            return {"result": False, "message": f"A book with the book id '{book_id}' from user with id '{user_id}' already exists in the wishlist."}
        else:
            new_withlist_book = WishlistBook.objects.create(
                user_id=user_id,
                book_id=book_id,
            )
            new_withlist_book.save()
            return {"result": True, "message": f"Book with id '{book_id}' from user with id '{user_id}' successfully added to the wishlist."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "message": f"Error adding book to wishlist: {e}"}


def remove_book_from_wishlist(user_id, book_id):
    try:
        if not WishlistBook.objects.filter(user_id=user_id, book_id=book_id).exists():
            return {"result": False, "message": f"The book with id '{book_id}' from user with id '{user_id}' does not exist in the wishlist."}
        else:
            withlist_book = WishlistBook.objects.get(
                user_id=user_id, book_id=book_id)
            withlist_book.delete()
            return {"result": True, "message": f"The book with id '{book_id}' from user with id '{user_id}' successfully removed from the wishlist."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "message": f"Error removing book from wishlist: {e}"}


def add_book_to_history(user_id, book_id):
    try:
        if BookProgress.objects.filter(user_id=user_id, book_id=book_id).exists():
            return {"result": False, "message": f"The book with id '{book_id}' from user with id '{user_id}' already exist in the history."}
        else:
            new_history_book = WishlistBook.objects.create(
                user_id=user_id,
                book_id=book_id,
            )
            new_history_book.save()
            return {"result": True, "message": f"The book with id '{book_id}' from user with id '{user_id}' successfully added to the history."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "message": f"Error adding book to history: {e}"}


def remove_book_from_history(user_id, book_id):
    try:
        if not BookProgress.objects.filter(user_id=user_id, book_id=book_id).exists():
            return {"result": False, "message": f"The book with id '{book_id}' from user with id '{user_id}' does not exist in the history."}
        else:
            history_book = BookProgress.objects.get(
                user_id=user_id, book_id=book_id)
            history_book.delete()
            return {"result": True, "message": f"The book with id '{book_id}' from user with id '{user_id}' successfully removed from the history."}
    except Exception as e:
        print(f"Exception: {e}")
        return {"result": False, "message": f"Error removing book from history: {e}"}
