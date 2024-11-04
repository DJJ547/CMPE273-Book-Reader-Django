# serializers.py
from rest_framework import serializers
from mysql_models.models import Book
from mysql_models.models import BookGenre

class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenre
        fields = ['book', 'genre']  # Only include book and genre fields

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # You can specify fields as needed
