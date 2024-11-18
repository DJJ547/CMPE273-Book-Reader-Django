from .mysql import fetch_shelves_data, fetch_wishlist_data, fetch_history_data, fetch_shelves_list_data, add_book_to_shelf, remove_book_from_shelf, add_shelf, remove_shelf, add_book_to_wishlist, remove_book_from_wishlist
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv
load_dotenv()


@api_view(['GET'])
def get_shelves_data_view(request):
    user_id = request.query_params.get('user_id', '')
    shelves_data = fetch_shelves_data(user_id)
    if not shelves_data['data']:
        return Response(shelves_data, status=status.HTTP_404_NOT_FOUND)
    return Response(shelves_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_wishlist_data_view(request):
    user_id = request.query_params.get('user_id', '')
    wishlist_data = fetch_wishlist_data(user_id)
    if not wishlist_data['data']:
        return Response(wishlist_data, status=status.HTTP_404_NOT_FOUND)
    return Response(wishlist_data, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_history_data_view(request):
    user_id = request.query_params.get('user_id', '')
    history_Data = fetch_history_data(user_id)
    if not history_Data['data']:
        return Response(history_Data, status=status.HTTP_404_NOT_FOUND)
    return Response(history_Data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_shelf_list_view(request):
    user_id = request.query_params.get('user_id', '')
    shelf_list = fetch_shelves_list_data(user_id)
    if not shelf_list['data']:
        return Response(shelf_list, status=status.HTTP_404_NOT_FOUND)
    return Response(shelf_list, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_shelf_view(request):
    user_id = request.data.get('user_id', '')
    shelf = request.data.get('shelf', '')
    result = add_shelf(user_id, shelf)
    if not result['data']:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_shelf_view(request):
    shelf_id = request.query_params.get('shelf_id', '')
    result = remove_shelf(shelf_id)
    if not result['data']:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_book_to_shelf_view(request):
    user_id = request.data.get('user_id', '')
    shelf_id = request.data.get('shelf_id', '')
    book_id = request.data.get('book_id', '')
    result = add_book_to_shelf(user_id, shelf_id, book_id)
    if not result['data']:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_book_from_shelf_view(request):
    shelf_id = request.data.get('shelf_id', '')
    book_id = request.data.get('book_id', '')
    result = remove_book_from_shelf(shelf_id, book_id)
    if not result['data']:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_book_to_wishlist_view(request):
    user_id = request.data.get('user_id', '')
    book_id = request.data.get('book_id', '')
    result = add_book_to_wishlist(user_id, book_id)
    if not result['data']:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_book_from_wishlist_view(request):
    user_id = request.data.get('user_id', '')
    book_id = request.data.get('book_id', '')
    result = remove_book_from_wishlist(user_id, book_id)
    if not result['data']:
        return Response(result, status=status.HTTP_404_NOT_FOUND)
    return Response(result, status=status.HTTP_200_OK)