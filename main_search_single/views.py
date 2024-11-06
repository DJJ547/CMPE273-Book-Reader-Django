from .serializers import BookSerializer,BookGenreSerializer
from mysql_models.models import Book,BookGenre
from rest_framework import generics,viewsets
from rest_framework.response import Response
from rest_framework import status
from django.db import connection
from rest_framework.views import APIView
from django.db.models import Q

class ListTablesView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES;")
            tables = cursor.fetchall()
        table_names = [table[0] for table in tables]
        return Response(table_names, status=status.HTTP_200_OK)

class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookSearchView(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return Book.objects.filter(book_name__icontains=query)  # Use book_name instead of title
        return Book.objects.all()

class BookGenreListView(APIView):
    def get(self, request, book_id=None):
        if book_id is not None:
            # Retrieve all BookGenre instances for the specified book_id
            genres = BookGenre.objects.filter(book_id=book_id)
        else:
            # Retrieve all BookGenre instances
            genres = BookGenre.objects.all()

        serializer = BookGenreSerializer(genres, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CombinedBookGenreListView(APIView):
    def get(self, request, book_id=None):
        if book_id:  # If a book ID is provided, return the single book
            return self.get_by_id(request, book_id)

        query = request.GET.get('q', None)  # Check if there's a search query
        if query:  # If a search query is provided, perform search
            return self.search(request, query)

        # If no parameters are given, retrieve all books
        return self.get_all_books(request)

    def get_all_books(self, request):
        # Retrieve all books
        books = Book.objects.all()
        books_data = BookSerializer(books, many=True).data

        # Retrieve all genres and organize them by book id
        genres = BookGenre.objects.all()
        genres_data = BookGenreSerializer(genres, many=True).data

        # Create a dictionary to associate genres with their respective books
        genre_dict = {}
        for genre in genres_data:
            book_id = genre['book']
            if book_id not in genre_dict:
                genre_dict[book_id] = []
            genre_dict[book_id].append(genre['genre'])

        # Combine book data with genres
        combined_data = []
        for book in books_data:
            book_id = book['id']
            book_genres = genre_dict.get(book_id, [])
            combined_entry = {
                "id": book['id'],
                "book_name": book['book_name'],
                "author": book['author'],
                "book_link": book['book_link'],
                "book_cover": book['book_cover'],
                "book_description": book['book_description'],
                "genres": book_genres
            }
            combined_data.append(combined_entry)

        return Response(combined_data, status=status.HTTP_200_OK)

    def get_by_id(self, request, book_id):
        # Retrieve a single book by ID
        try:
            book = Book.objects.get(id=book_id)
            book_data = BookSerializer(book).data
            
            # Retrieve genres for the book
            genres = BookGenre.objects.filter(book=book_id)
            genres_data = BookGenreSerializer(genres, many=True).data
            
            # Combine book data with genres
            book_genres = [genre['genre'] for genre in genres_data]
            book_data['genres'] = book_genres
            
            return Response(book_data, status=status.HTTP_200_OK)
        except Book.DoesNotExist:
            return Response({"error": "Book not found."}, status=status.HTTP_404_NOT_FOUND)

class CombinedBookGenreListViewSearch(generics.ListAPIView):
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', None)
        if query:
            return Book.objects.filter(
                Q(book_name__icontains=query) | 
                Q(author__icontains=query) | 
                Q(book_description__icontains=query)
            ).distinct()
        return Book.objects.all()

    def list(self, request, *args, **kwargs):
        # Call the original list method to get the queryset
        queryset = self.get_queryset()
        books_data = BookSerializer(queryset, many=True).data
        
        # Combine book data with genres
        combined_data = []
        for book in books_data:
            book_id = book['id']
            # Retrieve genres for the found book
            genres = BookGenre.objects.filter(book=book_id)
            genres_data = BookGenreSerializer(genres, many=True).data
            
            combined_entry = {
                "id": book['id'],
                "book_name": book['book_name'],
                "author": book['author'],
                "book_link": book['book_link'],
                "book_cover": book['book_cover'],
                "book_description": book['book_description'],
                "genres": [genre['genre'] for genre in genres_data]
            }
            combined_data.append(combined_entry)

        # Return a message if no books match the search query
        if not combined_data:
            return Response({"message": "No books found matching your search."}, status=status.HTTP_404_NOT_FOUND)

        return Response(combined_data, status=status.HTTP_200_OK)

