from distutils.util import execute
from multiprocessing import connection
from sqlite3 import Cursor
from app import app
from flask import request
from services.dbconnection import connect_and_commit
from models.model import Book
from flask import jsonify
import pymysql
from config import mydb
from services.auth import check_for_token
from services.log import logger

#INSERTING BOOK DETAILS
@app.route('/book', methods=['POST'])
@check_for_token
def addBook(isbn=None):
    try:
        json = request.json
        bookname= json['bookname'] 
        author = json['author']
        categoryid = json['categoryid']
        price = json['price']
        adminid=json['adminid']
        bookObj = Book(isbn,bookname, author, categoryid, price,adminid)
        if bookname and author and categoryid and price and adminid and request.method =='POST':           
            sqlQuery = "INSERT INTO book(bookname, author, categoryid, price, adminid) VALUES(%s, %s, %s, %s,%s)"
            bindData = (bookObj.bookname, bookObj.author, bookObj.categoryid, bookObj.price,bookObj.adminid)  
            connect_and_commit(sqlQuery, bindData)           
            respone = jsonify('Book details added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except pymysql.Error as e:
                logger.error(f"pymysql.Error: {e}")
                return jsonify({'error': 'Error occur in sql syntax'})         
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify({'error': 'A required key is missing from the request'})
    

# VIEWING ALL BOOKS
@app.route('/book', methods=['GET'])
@check_for_token
def book():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT bookname, author, categoryid, price, adminid FROM book")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except pymysql.Error as e:
        logger.error(f"pymysql.Error: {e}")
        return jsonify({'error': 'Error occur in sql syntax'})
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify({'error': 'A required key is missing from the request'})
    finally:
        cursor.close()
        conn.close()

# VIEWING PARTICULAR BOOK 
@app.route('/book/<isbn>', methods=['GET'])
@check_for_token
def bookDetails(isbn):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT bookname ,author, category,price,adminid FROM book WHERE isbn =%s", (isbn))
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except pymysql.Error as e:
        logger.error(f"pymysql.Error: {e}")
        return jsonify({'error': 'Error occur in sql syntax'})
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify({'error': 'A required key is missing from the request'})
    finally:
        cursor.close()
        conn.close()

#UPDATING THE BOOK DETAILS    
@app.route('/book/<isbn>', methods=['PUT'])
@check_for_token
def updateBook(isbn):
    try:
        _json = request.json
        print(_json)
        _bookname = _json['bookname']
        _author= _json['author']
        _categoryid = _json['categoryid']
        _price = _json['price']
        _adminid=_json['adminid']
        book= Book(isbn,_bookname, _author, _categoryid, _price,_adminid)
        if _bookname and _author and _categoryid and _price and _adminid and request.method  == 'PUT':           
            sqlQuery = ("UPDATE book SET bookname= %s, author= %s, categoryid= %s, price= %s,adminid=%s WHERE isbn=%s")
            bindData = (book.bookname,book.author, book.categoryid, book.price, book.adminid,isbn)
            connect_and_commit(sqlQuery, bindData) 
            respone = jsonify('Book Details updated successfully!')
            respone.status_code = 200
            print(respone)
            return respone
        else:
            return showMessage()
    except pymysql.Error as e:
        logger.error(f"pymysql.Error: {e}")
        return jsonify({'error': 'Error occur in sql syntax'})
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify({'error': 'A required key is missing from the request'})

# DELETING BOOK DETAILS
@app.route('/book/<isbn>', methods=['DELETE'])
@check_for_token
def deleteBook(isbn):
    try:            
        connect_and_commit("DELETE FROM book WHERE isbn =%s",(isbn))     
        respone = jsonify('Book Details deleted successfully!')
        respone.status_code = 200
        return respone
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify({'error': 'A required key is missing from the request'})


# SEARCHING FOR BOOKS
@app.route('/book',methods=['GET'])
@check_for_token
def searchBook(bookname):
    json = request.json
    bookname= json['bookname'] 
    author = json['author']
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT bookname, author from book WHERE bookname LIKE %s OR author LIKE %s",
        bindData = (author, bookname)
        cursor.execute(sqlQuery, bindData)
        books = cursor.fetchall()
        return jsonify(books)
    except pymysql.Error as e:
        logger.error(f"pymysql.Error: {e}")
        return jsonify({'error': 'Error occur in sql syntax'})

# UNIT TEST FOR ADD BOOK
# def AddBook(isbn,bookname, author, categoryid, price,adminid):
#     if not bookname or not author or not categoryid or not price:
#         response = jsonify({'message': 'All fields are required'})
#         response.status_code = 400
#         return response
#     conn = mydb.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)  
#     bookObj = Book(isbn,bookname, author, categoryid, price,adminid)
#     if bookname and author and categoryid and price and adminid and request.method =='POST':
#             print(bookObj.bookname)
#             sqlQuery = "INSERT INTO book(bookname, author, category, price,adminid) VALUES(%s, %s, %s, %s,%s)"
#             bindData = (bookObj.bookname, bookObj.author, bookObj.categoryid, bookObj.price,bookObj.adminid)
#             try:
#                 conn = mydb.connect()
#                 cursor = conn.cursor(pymysql.cursors.DictCursor)  
#                 print("GGGGG")
#                 data =cursor.execute(sqlQuery, bindData)
#                 print(data)
#                 conn.commit()
#                 print("fdgddddddddf")
#             except pymysql.Error as e:
#                 logger.error(f"pymysql.Error: {e}")
#                 return jsonify({'error': 'Error occur in sql syntax'})
           
#             respone = jsonify('Book details added successfully!')
#             respone.status_code = 200
#             return respone
#     else:
#         return showMessage()
 
@app.errorhandler(Exception)
def handle_error(error):
    return jsonify({'error': str(error)}), 500
#ERROR HANDLING
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone