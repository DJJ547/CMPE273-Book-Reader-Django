from django.urls import path
from .views import get_library_data_view, get_shelf_data_view, get_shelves_with_current_book_view, get_shelves_without_current_book_view, add_shelf_view, edit_shelf_view, remove_shelf_view, add_book_to_shelf_view, remove_book_from_shelf_view, add_book_to_wishlist_view, remove_book_from_wishlist_view, add_book_to_history_view, remove_book_from_history_view, get_current_book_history_view

urlpatterns = [
    path('get_library_data/', get_library_data_view, name='get user library data'),
    path('get_shelves_data/', get_shelf_data_view, name='get user shelves data'),
    path('get_shelves_with_current_book/', get_shelves_with_current_book_view, name='get a list of shelves that contains the current book'),
    path('get_shelves_without_current_book/', get_shelves_without_current_book_view, name='get a list of shelves that does not contain the current book'),
    path('add_shelf/', add_shelf_view, name='add a shelf'),
    path('edit_shelf/', edit_shelf_view, name='edit a shelf'),
    path('remove_shelf/', remove_shelf_view, name='remove a shelf'),
    path('add_book_to_shelf/', add_book_to_shelf_view, name='add a book to a shelf'),
    path('remove_book_from_shelf/', remove_book_from_shelf_view, name='remove a book from a shelf'),
    path('add_book_to_wishlist/', add_book_to_wishlist_view, name='add a book to the wishlist'),
    path('remove_book_from_wishlist/', remove_book_from_wishlist_view, name='remove a book from the wishlist'),
    path('add_book_to_history/', add_book_to_history_view, name='add a book to the history'),
    path('remove_book_from_history/', remove_book_from_history_view, name='remove a book from the history'),
    path('get_current_book_history/', get_current_book_history_view, name='get current book history')
]