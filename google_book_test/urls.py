from django.urls import path
from .views import get_books, get_books_paginated, get_specific_books, get_book_reviews, exchange_code, get_google_books_reading_list

urlpatterns = [
    path('get-books/', get_books, name='get_books'),
    path('get-books-paginated/', get_books_paginated, name='get_books_paginated'),
    path('get-specific-books/', get_specific_books, name='get_specific_books'),
    path('get-book-reviews/', get_book_reviews, name='get_book_reviews'),
    path('exchange-code/', exchange_code, name='exchange_code'),
    path('google-books/', get_google_books_reading_list, name='get_google_books_reading_list'),
]