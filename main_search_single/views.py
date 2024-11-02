# views.py
from .serializers import BookSerializer
from .models import Book
from rest_framework import generics
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


class ListTablesView(APIView):
    def get(self, request):
        with connection.cursor() as cursor:
            # The SQL command to retrieve table names
            cursor.execute("SHOW TABLES;")  # For MySQL
            tables = cursor.fetchall()

        # Extract table names from the results
        table_names = [table[0] for table in tables]

        return Response(table_names, status=status.HTTP_200_OK)


class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
