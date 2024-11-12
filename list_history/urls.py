from django.urls import path
from .views import get_reading_list_books_view, get_book_genres_view, change_favorite_view, delete_reading_list_view, create_reading_list_view, edit_reading_list_view

urlpatterns = [
    path('get_reading_list_books/', get_reading_list_books_view, name='get reading list books'),
    path('get_book_genres/', get_book_genres_view, name='get book genres'),
    path('change_favorite/', change_favorite_view, name='change favorite'),
    path('delete_reading_list/', delete_reading_list_view, name='delete reading list'),
    path('create_reading_list/', create_reading_list_view, name='create reading list'),
    path('edit_reading_list/', edit_reading_list_view, name='edit reading list')
]
