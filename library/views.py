from .mysql import fetch_library_data, fetch_shelves_list_data, fetch_shelves_with_current_book, fetch_shelves_without_current_book, add_book_to_shelf, remove_book_from_shelf, add_shelf, edit_shelf, remove_shelf, add_book_to_wishlist, remove_book_from_wishlist, add_book_to_history, remove_book_from_history, fetch_current_book_history
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv
load_dotenv()


@api_view(['GET'])
def get_library_data_view(request):
    user_id = request.query_params.get('user_id', '')
    library_data = fetch_library_data(user_id)
    if not library_data['data']:
        return Response(library_data, status=status.HTTP_404_NOT_FOUND)
    return Response(library_data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_shelf_list_view(request):
    user_id = request.query_params.get('user_id', '')
    shelf_list = fetch_shelves_list_data(user_id)
    if not shelf_list['data']:
        return Response(shelf_list, status=status.HTTP_404_NOT_FOUND)
    return Response(shelf_list, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_shelves_with_current_book_view(request):
    user_id = int(request.query_params.get('user_id', ''))
    book_id = int(request.query_params.get('book_id', ''))
    shelf_list = fetch_shelves_with_current_book(user_id, book_id)
    if not shelf_list['data']:
        return Response(shelf_list, status=status.HTTP_404_NOT_FOUND)
    return Response(shelf_list, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_shelves_without_current_book_view(request):
    user_id = int(request.query_params.get('user_id', ''))
    book_id = int(request.query_params.get('book_id', ''))
    shelf_list = fetch_shelves_without_current_book(user_id, book_id)
    if not shelf_list['data']:
        return Response(shelf_list, status=status.HTTP_404_NOT_FOUND)
    return Response(shelf_list, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_shelf_view(request):
    user_id = request.data.get('user_id', '')
    shelf = request.data.get('shelf', '')
    output = add_shelf(user_id, shelf)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['PUT'])
def edit_shelf_view(request):
    user_id = request.data.get('user_id', '')
    shelf = request.data.get('shelf', '')
    output = edit_shelf(user_id, shelf)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_shelf_view(request):
    user_id = request.query_params.get('user_id', '')
    shelf_id = request.query_params.get('shelf_id', '')
    output = remove_shelf(user_id, shelf_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_book_to_shelf_view(request):
    user_id = request.data.get('user_id', '')
    shelf_id = request.data.get('shelf_id', '')
    book_id = request.data.get('book_id', '')
    print(f"add book to shelf request processed with user_id: {user_id}, shelf_id: {shelf_id}, book_id: {book_id}")
    output = add_book_to_shelf(user_id, shelf_id, book_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_book_from_shelf_view(request):
    user_id = request.query_params.get('user_id', '')
    shelf_id = request.query_params.get('shelf_id', '')
    book_id = request.query_params.get('book_id', '')
    output = remove_book_from_shelf(user_id, shelf_id, book_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_book_to_wishlist_view(request):
    user_id = request.data.get('user_id', '')
    book_id = request.data.get('book_id', '')
    output = add_book_to_wishlist(user_id, book_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_book_from_wishlist_view(request):
    user_id = request.query_params.get('user_id', '')
    book_id = request.query_params.get('book_id', '')
    output = remove_book_from_wishlist(user_id, book_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['POST'])
def add_book_to_history_view(request):
    user_id = request.data.get('user_id', '')
    book_id = request.data.get('book_id', '')
    output = add_book_to_history(user_id, book_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def remove_book_from_history_view(request):
    user_id = request.query_params.get('user_id', '')
    book_id = request.query_params.get('book_id', '')
    output = remove_book_from_history(user_id, book_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_current_book_history_view(request):
    user_id = request.query_params.get('user_id', '')
    book_id = request.query_params.get('book_id', '')
    output = fetch_current_book_history(user_id, book_id)
    if not output['result']:
        return Response(output, status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)