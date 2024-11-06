from django.urls import path
from .views import get_reading_lists, get_book_genres

urlpatterns = [
    path('get_reading_lists/', get_reading_lists, name='get_reading_lists'),
    path('get_book_genres/', get_book_genres, name='get_book_genres'),
]
