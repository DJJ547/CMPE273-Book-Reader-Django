# urls.py
from .views import BookListView
from django.urls import path
from .views import ListTablesView

urlpatterns = [
    path('tables/', ListTablesView.as_view(), name='list-tables'),
    path('books/', BookListView.as_view(), name='book-list'),

    # Add other paths as necessary
]
# urls.py
