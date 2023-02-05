import unittest
from unittest.mock import Mock
import json
from flask import Flask
# from sevices.admin.book import AddBook
from services.user.register import register_test

app = Flask(__name__)

class AddBookTestCase(unittest.TestCase):
    def setUp(self):
        self.isbn= 123467543211
        self.bookname= "Two states"
        self.author="Chetan Bagat"
        self.category=6
        self.price=1000
        self.adminid=2
        self.request = Mock(method='POST')


# def test_add_book_success(self):
#     with app.app_context():
#         # response = AddBook(self.isbn, self.bookname, self.author, self.category, self.price, self.adminid, self.request)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.get_json(), {"message": "Book Details added successfully!"})

# def test_add_book_missing_key(self):
#     with app.app_context():
#         # response = AddBook(self.isbn, "", "","", "","" ,self.request)
#         self.assertEqual(response.get_json(), {"message": "All fields are required"})



if __name__ == '__main__':
    unittest.main()








































#     def test_add_book_success(self):
#         with self.app.test_request_context(
#             method='POST',
#             data=json.dumps({
#                 'bookname': 'Test Book',
#                 'author': 'Test Author',
#                 'category': 'Test Category',
#                 'price': 10.0
#             }),
#             headers={'Content-Type': 'application/json'}
#         ):
#             response = addBook()
#             self.assertEqual(response.status_code, 200)
#             self.assertEqual(response.get_json(), {'message': 'Book details added successfully!'})

#     def test_add_book_missing_key(self):
#         with self.app.test_request_context(
#             method='POST',
#             data=json.dumps({
#                 'bookname': 'Test Book',
#                 'author': 'Test Author',
#                 'category': 'Test Category'
#             }),
#             headers={'Content-Type': 'application/json'}
#         ):
#             response = addBook()
#             self.assertEqual(response.status_code, 400)
#             self.assertEqual(response.get_json(), {'error': 'A required key is missing from the request'})

# if __name__ == '__main__':
#     unittest.main()
