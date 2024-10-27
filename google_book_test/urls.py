from django.urls import path
from .views import search_books, fetch_book_content, get_books_by_genre, get_book_reviews, get_google_books_reading_list

urlpatterns = [
    path('search-books/', search_books, name='get_books'),
    path('fetch-book-content/', fetch_book_content, name='fetch_book_content'),
    path('get-books-by-genre/', get_books_by_genre, name='get_books_by_genre'),
    path('get-book-reviews/', get_book_reviews, name='get_book_reviews'),
    path('google-books/', get_google_books_reading_list, name='get_google_books_reading_list'),
]