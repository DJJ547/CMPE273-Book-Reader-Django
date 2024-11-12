from mysql_models.models import Book, ReadingList, ReadingListBook, BookGenre

def fetch_reading_list_books_With_meta_genres(user_id):
    try:
        lists_data_map = {}
        reading_lists = ReadingList.objects.filter(user_id=user_id)
        for reading_list in reading_lists:
            lists_data_map[reading_list.id] = {
                "id": reading_list.id,
                "name": reading_list.name,
                "description": reading_list.description,
                "created_at": reading_list.created_at,
                "updated_at": reading_list.updated_at,
                "flag_color": reading_list.flag_color,
                "icon": reading_list.icon,
                "is_favorite": reading_list.is_favorite,
            }
            list_books_data = []
            reading_list_books = ReadingListBook.objects.filter(reading_list_id=reading_list.id)
            for reading_list_book in reading_list_books:
                list_book_data = fetch_book_meta(reading_list.id, reading_list_book.book_id)
                list_books_data.append(list_book_data)
            lists_data_map[reading_list.id]['books'] = list_books_data
        return lists_data_map
    except Exception as e:
        print("An error occurred:", e)
        return []
    
def fetch_book_meta(list_id, book_id):
    try:
        book_meta = Book.objects.get(id=book_id)
        book_status = fetch_book_stat(list_id, book_id)
        list_book_data = {
            "book_id": book_id,
            "book_name": book_meta.book_name,
            "author": book_meta.author,
            "book_link": book_meta.book_link,
            "book_cover":book_meta.book_cover,
            "book_description": book_meta.book_description,
            "num_of_chapters": book_meta.num_of_chapters,
            "added_at": book_status['added_at'],
            "status": book_status['status'],
            "genres": fetch_book_genres(book_id),
        }
        return list_book_data
    except Exception as e:
        print("An error occurred:", e)
        return []
    
def fetch_book_stat(list_id, book_id):
    try:
        book_stat = ReadingListBook.objects.get(reading_list_id=list_id, book_id=book_id)
        book_stat_data = {
            "added_at": book_stat.added_at,
            "status": book_stat.status,
        }
        return book_stat_data
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

def swap_favorite(list_id):
    try:
        reading_list = ReadingList.objects.get(id=list_id)
        # Optionally, convert to a list of dictionaries or another format
        reading_list.is_favorite = not reading_list.is_favorite
        reading_list.save()
        return reading_list.is_favorite
    except Exception as e:
        print("An error occurred:", e)
        return None
    
def delete_booklist_by_id(id):
    try:
        booklist = ReadingList.objects.get(id=id)
        booklist.delete()
        return True
    except ReadingList.DoesNotExist:
        return False

def create_booklist(user_id, name, description, is_favorite, icon, color):
    try:
        if ReadingList.objects.filter(user_id=user_id, name=name).exists():
            message = f"A reading list with the name '{name}' already exists."
            print(message)
            return {"output": False, "message": message}
        new_booklist = ReadingList.objects.create(
            name=name,
            user_id=user_id,
            description=description,
            is_favorite=bool(is_favorite),
            icon=icon,
            flag_color=color
        )
        message = "Reading list successfully created!"
        print(message)
        new_booklist.save()
        return {"output": True, "message": message}
    except Exception as e:
        message = f"Error creating reading list: {e}"
        print(message)
        return {"output": False, "message": message}
    
def edit_booklist_by_id(id, user_id, name=None, description=None, is_favorite=None, icon=None, color=None):
    try:
        booklist = ReadingList.objects.get(id=id, user_id=user_id)
        if name is not None:
            booklist.name = name
        if description is not None:
            booklist.description = description
        if is_favorite is not None:
            booklist.is_favorite = bool(is_favorite)
        if icon is not None:
            booklist.icon = icon
        if color is not None:
            booklist.flag_color = color
        booklist.save()
        return True, "Reading list updated successfully."
    except ReadingList.DoesNotExist:
        return False, "Reading list not found."
    except Exception as e:
        return False, f"An error occurred: {e}"
