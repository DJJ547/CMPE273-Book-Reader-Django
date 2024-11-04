# serializers.py
from rest_framework import serializers
from mysql_models.models import Book


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # You can specify fields as needed
