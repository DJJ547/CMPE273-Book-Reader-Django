from django.urls import path
from .views import get_shelves_data_view, get_wishlist_data_view, get_history_data_view, get_shelf_list_view, add_shelf_view, remove_shelf_view, add_book_to_shelf_view, remove_book_from_shelf_view, add_book_to_wishlist_view, remove_book_from_wishlist_view

urlpatterns = [
    path('get_shelves_data/', get_shelves_data_view, name='get user shelves data'),
    path('get_wishlist_data/', get_wishlist_data_view, name='get user wishlist data'),
    path('get_history_data/', get_history_data_view, name='get user history data'),
    path('get_shelf_list/', get_shelf_list_view, name='get a list of shelves'),
    path('add_shelf/', add_shelf_view, name='add a shelf'),
    path('remove_shelf/', remove_shelf_view, name='remove a shelf'),
    path('add_book_to_shelf/', add_book_to_shelf_view, name='add a book to a shelf'),
    path('remove_book_from_shelf/', remove_book_from_shelf_view, name='remove a book from a shelf'),
    path('add_book_to_wishlist/', add_book_to_wishlist_view, name='add a book to the wishlist'),
    path('remove_book_from_wishlist/', remove_book_from_wishlist_view, name='remove a book from the wishlist'),
]