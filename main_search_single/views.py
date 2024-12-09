from .serializers import BookSerializer,BookGenreSerializer,BookReviewSerializer
from mysql_models.models import Book,BookGenre,BookReview,BookChapter, CustomUser
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


        # Retrieve all users and create a dictionary of user_id to email
        users = CustomUser.objects.all().values('id', 'email')
        user_dict = {user['id']: user['email'] for user in users}

        # Retrieve all reviews and organize them by book id
        reviews = BookReview.objects.all()
        reviews_dict = {}
        for review in reviews:
            book_id = review.book_id
            if book_id not in reviews_dict:
                reviews_dict[book_id] = []

            # Use the user_id directly to get the username from user_dict
            email = user_dict.get(review.user_id, "unknown")  # No need to access .id here
            
            reviews_dict[book_id].append({
                "review": review.review,
                "rating": review.rating,
                "username": email
            })

        # Retrieve all chapters and organize them by book id
        chapters = BookChapter.objects.all().values('book_id', 'chapter_number', 'chapter_title')
        chapters_dict = {}
        for chapter in chapters:
            book_id = chapter['book_id']
            if book_id not in chapters_dict:
                chapters_dict[book_id] = []
            chapters_dict[book_id].append({
                "chapter_number": chapter['chapter_number'],
                "chapter_title": chapter['chapter_title']
            })

        # Create a dictionary to associate genres with their respective books
        genre_dict = {}
        for genre in genres_data:
            book_id = genre['book']
            if book_id not in genre_dict:
                genre_dict[book_id] = []
            genre_dict[book_id].append(genre['genre'])

        # Combine book data with genres, reviews, and chapters
        combined_data = []
        for book in books_data:
            book_id = book['id']
            book_genres = genre_dict.get(book_id, [])
            book_reviews = reviews_dict.get(book_id, [])
            book_chapters = chapters_dict.get(book_id, [])
            combined_entry = {
                "id": book['id'],
                "book_name": book['book_name'],
                "author": book['author'],
                "book_link": book['book_link'],
                "book_cover": book['book_cover'],
                "book_description": book['book_description'],
                "genres": book_genres,
                "reviews": book_reviews,
                "chapters": book_chapters  # Adding chapters to the combined entry
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

            # Fetch all users and map user_id to username
            users = CustomUser.objects.all().values('id', 'email')
            user_dict = {user['id']: user['email'] for user in users}

            # Retrieve reviews for the book and map user_id to username
            reviews = BookReview.objects.filter(book_id=book_id)
            reviews_data = []
            for review in reviews:
                email = user_dict.get(review.user_id, "unknown")  # Get the username using user_dict
                reviews_data.append({
                    "review": review.review,
                    "rating": review.rating,
                    "username": email
                })

            # Retrieve chapters for the book
            chapters = BookChapter.objects.filter(book_id=book_id).values('chapter_number', 'chapter_title')
            chapters_data = [{"chapter_number": chapter['chapter_number'], "chapter_title": chapter['chapter_title']} for chapter in chapters]

            # Combine book data with genres, reviews, and chapters
            book_genres = [genre['genre'] for genre in genres_data]
            book_data['genres'] = book_genres
            book_data['reviews'] = reviews_data
            book_data['chapters'] = chapters_data  # Adding chapters to the response data

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

        # Fetch all users and map user_id to username
        users = CustomUser.objects.all().values('id', 'email')
        user_dict = {user['id']: user['email'] for user in users}

        # Combine book data with genres, reviews, and chapters
        combined_data = []
        for book in books_data:
            book_id = book['id']
            
            # Retrieve genres for the found book
            genres = BookGenre.objects.filter(book=book_id)
            genres_data = BookGenreSerializer(genres, many=True).data
            
            # Retrieve reviews for the found book and map user_id to username
            reviews = BookReview.objects.filter(book_id=book_id)
            reviews_data = []
            for review in reviews:
                email = user_dict.get(review.user_id, "unknown")  # Get the username using user_dict
                reviews_data.append({
                    "review": review.review,
                    "rating": review.rating,
                    "username": email
                })
            
            # Retrieve chapters for the found book
            chapters = BookChapter.objects.filter(book_id=book_id).values('chapter_number', 'chapter_title')
            chapters_data = [{"chapter_number": chapter['chapter_number'], "chapter_title": chapter['chapter_title']} for chapter in chapters]
            
            # Combine all the data into a single entry
            combined_entry = {
                "id": book['id'],
                "book_name": book['book_name'],
                "author": book['author'],
                "book_link": book['book_link'],
                "book_cover": book['book_cover'],
                "book_description": book['book_description'],
                "genres": [genre['genre'] for genre in genres_data],
                "reviews": reviews_data,  # Add reviews with usernames
                "chapters": chapters_data   # Add chapters
            }
            combined_data.append(combined_entry)

        # Return a message if no books match the search query
        if not combined_data:
            return Response({"message": "No books found matching your search."}, status=status.HTTP_404_NOT_FOUND)

        return Response(combined_data, status=status.HTTP_200_OK)

class BookReviewCreateView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            book_id = int(request.data.get('book_id'))
            user_id = int(request.data.get('user_id'))
            review = request.data.get('review', '')
            rating = request.data.get('rating', '')
            new_review = BookReview.objects.create(
                book_id=book_id,
                user_id=user_id,
                review=review,
                rating=rating
            )
            new_review.save()
            new_review_data = {
                "book_id":new_review.book_id,
                "user_id":new_review.user_id,
                "review":new_review.review,
                "rating":new_review.rating
            }
            return Response(new_review_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(f"Exception: {e}")
            return Response(e, status=status.HTTP_400_BAD_REQUEST)
        # print(request.data)
        # serializer = BookReviewSerializer(data=request.data)
        # if serializer.is_valid():
        #     print("saved")
        #     # Save the new review to the database
        #     serializer.save()
        #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
