from distutils import errors
from getpass import getuser
from http.client import responses
from os import abort
import pymysql
import json
from config import mydb
from flask import jsonify
from flask import flash, request
from app import app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin
# CREATING CONSTRUCTOR
class Category:
    def __init__(self,categoryid,category):
        self.categoryid=categoryid
        self.category=category
# CREATING CONSTRUCTOR FOR BOOK
class Book:
    def __init__(self,bookname , author, category, price):
        self.bookname=bookname
        self.author=author
        self.price=price
        self.category=category        
# CREATING CATEGORY DETAILS
@app.route('/insertcategory', methods=['POST'])
def addCategory(categoryid=None):
    try:
        json = request.json
        category=json['category']
        categoryobj = Category(categoryid, category)
        if category and request.method =='POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO category(category) VALUES(%s)"
            bindData = categoryobj.category
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Category details added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'
#INSERTING BOOK DETAILS
@app.route('/insertbook', methods=['POST'])
def addBook(isbn=None):
    try:
        json = request.json
        bookname= json['bookname'] 
        author = json['author']
        category = json['category']
        price = json['price']
        print(price)
        bookObj = Book(bookname, author, category, price)
        if bookname and author and category and price and request.method =='POST':
            print("gdgdgwe")
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO book(bookname, author, category, price) VALUES(%s, %s, %s, %s)"
            bindData = (bookObj.bookname, bookObj.author, bookObj.category, bookObj.price)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('Book details added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception' 
# VIEWING ALL BOOKS
@app.route('/book', methods =['GET'])
def book():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT bookname,author, category,price FROM book")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e: 
        print(e)
    finally:
        cursor.close() 
        conn.close() 
# VIEWING PARTICULAR BOOK 
@app.route('/book/<isbn>', methods=['GET'])
def bookDetails(isbn):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT bookname ,author, category,price FROM book WHERE isbn =%s", (isbn))
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
#UPDATING THE BOOK DETAILS    
@app.route('/book/<isbn>', methods=['PUT'])
def updateBook(isbn):
    try:
        newjson = request.json
        newbookname = newjson['book_name']
        newauthor= newjson['author']
        newcategory = newjson['category']
        newprice = newjson['price']
        book = Book(newbookname, newauthor, newcategory, newprice)
        if isbn and newbookname and newauthor and newcategory and  newprice  and request.method  == 'PUT':           
            sqlQuery = ("UPDATE book SET bookname= %s, author= %s, category= %s, price= %s WHERE isbn=%s", (isbn))
            bindData = (book.bookname, book.author, book.category, book.price)
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
    except Exception as e:
        print(e)
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

# RUN SERVER
if __name__ == "__main__":
    app.run()


        
            
