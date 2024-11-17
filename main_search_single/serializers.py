# serializers.py
from rest_framework import serializers
from mysql_models.models import Book, BookReview
from mysql_models.models import BookGenre

class BookGenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookGenre
        fields = ['book', 'genre']  # Only include book and genre fields

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # You can specify fields as needed


class BookReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookReview
        fields = ['book_id', 'user_id', 'review', 'rating']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value