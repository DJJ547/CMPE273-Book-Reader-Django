from .mysql import fetch_reading_list_books_With_meta_genres, fetch_book_genres, swap_favorite, delete_booklist_by_id, create_booklist, edit_booklist_by_id
from rest_framework import status
from django.contrib.auth.decorators import login_required
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os
from dotenv import load_dotenv
load_dotenv()


@api_view(['GET'])
def get_reading_list_books_view(request):
    user_id = request.query_params.get('user_id', '')
    reading_lists = fetch_reading_list_books_With_meta_genres(user_id)
    if not reading_lists:
        return Response(
            {'reading_lists': [], 'message': 'No books found for the given query.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response({'reading_lists': reading_lists}, status=status.HTTP_200_OK)


@api_view(['GET'])
def get_book_genres_view(request):
    book_id = request.query_params.get('book_id', '')
    book_genres = fetch_book_genres(book_id)
    if not book_genres:
        return Response(
            {'book_genres': [], 'message': 'No books found for the given query.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response({'book_genres': book_genres}, status=status.HTTP_200_OK)


@api_view(['PUT'])
def change_favorite_view(request):
    booklist_id = request.data.get('booklist_id', '')
    state = swap_favorite(booklist_id)
    if state is None:
        return Response(
            {'state': state,
                'message': 'Failed to change favorite.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response({'change_succeed': state}, status=status.HTTP_200_OK)


@api_view(['DELETE'])
def delete_reading_list_view(request):
    booklist_id = request.query_params.get('booklist_id', '')
    print(booklist_id)
    # Assume this function deletes the resource
    success = delete_booklist_by_id(booklist_id)
    if not success:
        return Response(
            {'message': 'Failed to delete the reading list.'},
            status=status.HTTP_404_NOT_FOUND
        )
    return Response({'message': 'Reading list deleted successfully.'}, status=status.HTTP_200_OK)


@api_view(['POST'])
def create_reading_list_view(request):
    user_id = request.data.get('user_id', '')
    print(user_id)
    reading_list_data = request.data.get('list', '')
    name = reading_list_data.get('name', '')
    description = reading_list_data.get('description', '')
    is_favorite = reading_list_data.get('is_favorite', '')
    icon = reading_list_data.get('icon', '')
    color = reading_list_data.get('color', '')
    output = create_booklist(user_id, name, description, is_favorite, icon, color)
    if not output["output"]:
        return Response(output,status=status.HTTP_404_NOT_FOUND)
    return Response(output, status=status.HTTP_200_OK)


@api_view(['PUT'])
def edit_reading_list_view(request):
    user_id = request.data.get('user_id', '')
    id = request.data.get('reading_list_id')  # Assuming the ID is passed to identify the reading list
    if not id:
        return Response({"message": "ID is required."}, status=status.HTTP_400_BAD_REQUEST)

    # Extract optional parameters
    reading_list_data = request.data.get('list', '')
    name = reading_list_data.get('name', '')
    description = reading_list_data.get('description', '')
    is_favorite = reading_list_data.get('is_favorite', '')
    icon = reading_list_data.get('icon', '')
    color = reading_list_data.get('color', '')

    # Call the function to edit the reading list
    success, message = edit_booklist_by_id(id, user_id, name, description, is_favorite, icon, color)

    if not success:
        return Response({"message": message}, status=status.HTTP_404_NOT_FOUND)
    return Response({"message": message}, status=status.HTTP_200_OK)
