import unittest
from unittest.mock import Mock
import json
from flask import Flask
from model.admin.book import AddBook
from model.user.register import register_test

app = Flask(__name__)

class AddBookTestCase(unittest.TestCase):
    def setUp(self):
        self.isbn= 123467543211
        self.bookname= "Two states"
        self.author="Chetan Bagat"
        self.category=6
        self.price=1000
        self.request = Mock(method='POST')


def test_add_book_success(self):
    with app.app_context():
        response = AddBook(self.isbn, self.bookname, self.author, self.category, self.price, self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "Book Details added successfully!"})

def test_add_book_missing_key(self):
    with app.app_context():
        response = AddBook(self.isbn, "", "","", "", self.request)
        self.assertEqual(response.get_json(), {"message": "All fields are required"})



if __name__ == '__main__':
    unittest.main()








































