from app import app
from flask import request
from classes import Book
from flask import jsonify
import pymysql
from config import mydb
from auth import check_for_token
from log import logger

#INSERTING BOOK DETAILS
@app.route('/book', methods=['POST'])
@check_for_token
def addBook(isbn=None):
    try:
        json = request.json
        bookname= json['bookname'] 
        author = json['author']
        category = json['category']
        price = json['price']
        bookObj = Book(isbn,bookname, author, category, price)
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)      
        if bookname and author and category and price and request.method =='POST':
            sqlQuery = "INSERT INTO book(bookname, author, category, price) VALUES( %s, %s, %s,%s)"
            bindData = (bookObj.bookname, bookObj.author, bookObj.category, bookObj.price)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Book details added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except pymysql.Error as e:
        return handle_error(e)
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
        cursor.execute("SELECT bookname,author, category,price FROM book")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except pymysql.Error as e:
        return handle_error(e)
    except KeyError as e:
        return jsonify({'error': 'A required key is missing from the request'}), 400
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
        cursor.execute("SELECT bookname ,author, category,price FROM book WHERE isbn =%s", (isbn))
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except pymysql.Error as e:
        return handle_error(e)
    except KeyError as e:
        return jsonify({'error': 'A required key is missing from the request'}), 400
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
        _category = _json['category']
        _price = _json['price']
        book= Book(isbn,_bookname, _author, _category, _price)
        if _bookname and _author and _category and _price and request.method  == 'PUT':           
            sqlQuery = ("UPDATE book SET bookname= %s, author= %s, category= %s, price= %s WHERE isbn=%s")
            bindData = (book.bookname,book.author, book.category,book.price,isbn)
            conn = mydb.connect()
            cursor = conn.cursor()
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            respone = jsonify('Book Details updated successfully!')
            respone.status_code = 200
            print(respone)
            return respone
        else:
            return showMessage()
    except pymysql.Error as e:
        return handle_error(e)
    except KeyError as e:
        return jsonify({'error': 'A required key is missing from the request'}), 400
# DELETING BOOK DETAILS
@app.route('/book/<isbn>', methods=['DELETE'])
@check_for_token
def deleteBook(isbn):
    try:
        conn = mydb.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM book WHERE isbn =%s",(isbn))
        conn.commit()
        respone = jsonify('Book Details deleted successfully!')
        respone.status_code = 200
        return respone
    except KeyError as e:
        return jsonify({'error': 'A required key is missing from the request'}), 400
    finally:
        cursor.close()
        conn.close()
@app.route('/book/search',methods=['GET'])
@check_for_token
def searchBook():
    json = request.json
    bookname= json['bookname'] 
    author = json['author']
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        sqlQuery = "SELECT name, author from book WHERE name LIKE %s OR author LIKE %s",
        bindData = (author, bookname)
        cursor.execute(sqlQuery, bindData)
        books = cursor.fetchall()
        return jsonify(books)
    except pymysql.Error as e:
        return handle_error(e)

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
