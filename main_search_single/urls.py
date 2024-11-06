from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookListView, BookDetailView, ListTablesView, BookSearchView, BookGenreListView, CombinedBookGenreListView,CombinedBookGenreListViewSearch


urlpatterns = [
    path('tables/', ListTablesView.as_view(), name='list-tables'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/search/', BookSearchView.as_view(), name='book-search'),  # New path for search
    path('books/genres/', BookGenreListView.as_view(), name='book-genres'),
    path('books/genres/<int:book_id>/', BookGenreListView.as_view(), name='book-genres-by-id'),  # Get genres by book_id
    path('books/with-genres/search/', CombinedBookGenreListViewSearch.as_view(), name='search-books'),  # For searching books
    path('books/with-genres/<int:book_id>/', CombinedBookGenreListView.as_view(), name='single-book'),  # For getting a single book
    path('books/with-genres/', CombinedBookGenreListView.as_view(), name='combined-book-genre-list'),  # For getting all books
]
