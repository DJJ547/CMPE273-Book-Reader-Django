import requests
import os
from dotenv import load_dotenv
load_dotenv()
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
from rest_framework import status
import json

from .mysql import fetch_reading_lists, fetch_book_genres


@api_view(['GET'])
def get_reading_lists(request):
    user_id = request.GET.get('user_id', '')
    reading_lists = fetch_reading_lists(user_id)
    if not reading_lists:
        return Response(
            {'reading_lists': [], 'message': 'No books found for the given query.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response({'reading_lists': reading_lists}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_book_genres(request):
    book_id = request.GET.get('book_id', '')
    book_genres = fetch_book_genres(book_id)
    if not book_genres:
        return Response(
            {'book_genres': [], 'message': 'No books found for the given query.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response({'book_genres': book_genres}, status=status.HTTP_200_OK)
