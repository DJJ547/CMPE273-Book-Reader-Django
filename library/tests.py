from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch


class LibraryAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user_id = 1
        self.shelf_id = 1
        self.book_id = 1
        self.base_data = {"user_id": self.user_id}

    @patch('library.mysql.fetch_library_data')
    def test_get_library_data_view(self, mock_fetch):
        mock_fetch.return_value = {"data": {"Shelves": []},
                                   "message": "Library data fetched successfully."}
        response = self.client.get(reverse('get user library data'), {
                                   'user_id': self.user_id})
        self.assertEqual(response.status_code, 200)

    @patch('library.mysql.fetch_shelves_data')
    def test_get_shelves_data_view(self, mock_fetch):
        mock_fetch.return_value = {"data": [{"A Shelf": {}}],
                                   "message": "Shelves fetched successfully."}
        response = self.client.get(reverse('get user shelves data'), {
                                   'user_id': self.user_id})
        self.assertEqual(response.status_code, 204)

    @patch('library.mysql.fetch_shelves_with_current_book')
    def test_get_shelves_with_current_book_view(self, mock_fetch):
        mock_fetch.return_value = {"data": [{"A Shelf": {}}],
                                   "message": "Shelves fetched successfully."}
        response = self.client.get(reverse('get a list of shelves that contains the current book'), {
                                   'user_id': self.user_id, 'book_id': self.book_id})
        self.assertEqual(response.status_code, 204)

    @patch('library.mysql.add_shelf')
    def test_add_shelf_view(self, mock_add_shelf):
        # Mock the database function
        mock_add_shelf.return_value = {
            "result": True, 
            "message": "Shelf added successfully."
        }

        # Send the POST request with JSON data
        response = self.client.post(
            reverse('add a shelf'),
            data={'user_id': self.user_id, 'shelf': {'name': 'New Shelf', 'icon': 'key', 'background_color': '#FFFFFF'}},
            content_type='application/json'
        )

        # Assert the response status code
        self.assertEqual(response.status_code, 200)

    @patch('library.mysql.edit_shelf')
    def test_edit_shelf_view(self, mock_edit_shelf):
        mock_edit_shelf.return_value = {
            "result": True, "message": "Shelf edited successfully."}
        response = self.client.post(
            reverse('add a shelf'),
            data={'user_id': self.user_id, 'shelf': {'name': 'New Shelf', 'icon': 'key', 'background_color': '#FFFFFF'}},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)

    @patch('library.mysql.remove_shelf')
    def test_remove_shelf_view(self, mock_remove_shelf):
        mock_remove_shelf.return_value = {
            "result": True, "message": "Shelf removed successfully."}
        response = self.client.delete(
            f"{reverse('remove a shelf')}?user_id={self.user_id}&shelf_id={self.shelf_id}"
        )
        self.assertEqual(response.status_code, 400)

    @patch('library.mysql.add_book_to_shelf')
    def test_add_book_to_shelf_view(self, mock_add_book):
        mock_add_book.return_value = {
            "result": True, "message": "Book added to shelf."}
        response = self.client.post(reverse('add a book to a shelf'), {
                                    'user_id': self.user_id, 'shelf_id': self.shelf_id, 'book_id': self.book_id})
        self.assertEqual(response.status_code, 200)

    @patch('library.mysql.remove_book_from_shelf')
    def test_remove_book_from_shelf_view(self, mock_remove_book):
        mock_remove_book.return_value = {
            "result": True, "message": "Book removed from shelf."}
        response = self.client.delete(
            f"{reverse('remove a book from a shelf')}?user_id={self.user_id}&shelf_id={self.shelf_id}&book_id={self.book_id}"
        )
        self.assertEqual(response.status_code, 400)

    @patch('library.mysql.add_book_to_wishlist')
    def test_add_book_to_wishlist_view(self, mock_add_to_wishlist):
        mock_add_to_wishlist.return_value = {
            "result": True, "message": "Book added to wishlist."}
        response = self.client.post(reverse('add a book to the wishlist'), {
                                    'user_id': self.user_id, 'book_id': self.book_id})
        self.assertEqual(response.status_code, 200)

    @patch('library.mysql.remove_book_from_wishlist')
    def test_remove_book_from_wishlist_view(self, mock_remove_from_wishlist):
        mock_remove_from_wishlist.return_value = {
            "result": True, "message": "Book removed from wishlist."}
        response = self.client.delete(
            f"{reverse('remove a book from the wishlist')}?user_id={self.user_id}&book_id={self.book_id}"
        )
        self.assertEqual(response.status_code, 400)

    @patch('library.mysql.fetch_current_book_history')
    def test_get_current_book_history_view(self, mock_fetch_history):
        mock_fetch_history.return_value = {"result": True, "data": {
            "book_id": self.book_id, "current_chapter": 1}}
        response = self.client.get(reverse('get current book history'), {
                                   'user_id': self.user_id, 'book_id': self.book_id})
        self.assertEqual(response.status_code, 200)

    @patch('library.mysql.update_last_read_chapter')
    def test_update_book_history_view(self, mock_update_history):
        mock_update_history.return_value = {
            "result": True, "message": "Book history updated."}
        response = self.client.put(reverse('update book history'), {
                                   'user_id': self.user_id, 'book_name': 'Test Book', 'chapter_id': 1})
        self.assertEqual(response.status_code, 415)
