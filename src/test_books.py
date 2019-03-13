import unittest
import os
import json
from app import create_app, db


class BookTestCase(unittest.TestCase):
    """This class represents the books test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.book = {
            'name': 'How to python',
            'author': 'Python Man',
            'rank': 4,
            'date_finished': '2014-03-27'
        }

        # binds the app to the current context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def test_book_creation(self):
        """Test API can create a book (POST request)"""
        res = self.client().post('/books/', data=self.book)
        self.assertEqual(res.status_code, 201)
        self.assertIn('How to python', str(res.data))

    def test_api_can_get_all_books(self):
        """Test API can get a books (GET request)."""
        res = self.client().post('/books/', data=self.book)
        self.assertEqual(res.status_code, 201)
        res = self.client().get('/books/')
        self.assertEqual(res.status_code, 200)
        self.assertIn('How to python', str(res.data))

    def test_api_can_get_book_by_id(self):
        """Test API can get a single book by using it's id."""
        rv = self.client().post('/books/', data=self.book)
        self.assertEqual(rv.status_code, 201)
        result_in_json = json.loads(rv.data.decode('utf-8').replace("'", "\""))
        result = self.client().get(
            '/books/{}'.format(result_in_json['id']))
        self.assertEqual(result.status_code, 200)
        self.assertIn('How to python', str(result.data))

    def test_book_can_be_edited(self):
        """Test API can edit an existing book. (PUT request)"""
        rv = self.client().post(
            '/books/',
            data=self.book)
        self.assertEqual(rv.status_code, 201)
        rv = self.client().put(
            '/books/1',
            data={
                "rank": 7
            })
        self.assertEqual(rv.status_code, 200)
        results = self.client().get('/books/1')
        self.assertIn('7', str(results.data))

    def test_book_deletion(self):
        """Test API can delete an existing book. (DELETE request)."""
        rv = self.client().post(
            '/books/',
            data=self.book)
        self.assertEqual(rv.status_code, 201)
        res = self.client().delete('/books/1')
        self.assertEqual(res.status_code, 200)
        # Test to see if it exists, should return a 404
        result = self.client().get('/books/1')
        self.assertEqual(result.status_code, 404)

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
