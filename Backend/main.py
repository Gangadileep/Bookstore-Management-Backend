from distutils import errors
from getpass import getuser
from http.client import responses
from os import abort
import pymysql
import json
from config import mydb
from flask import jsonify
from flask import flash, request
from dbconnection import connect_and_commit
from app import app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin
# CREATING CONSTUCTOR 
class Usertype:
    def __init__(self,id,type):
        self.id=id
        self.type=type
# CREATING CONSTRUCTOR FOR REGISTER
class Register:
    def __init__(self,fullname,username,password,type):
        self.fullname=fullname
        self.username=username
        self.password=password
        self.type=type
# CREATING CONSTRUCTOR
class Category:
    def __init__(self,categoryid,category):
        self.categoryid=categoryid
        self.category=category
# CREATING CONSTRUCTOR FOR BOOK
class Book:
    def __init__(self,bookname, author, category, price):
        self.bookname=bookname
        self.author=author
        self.price=price
        self.category=category
#INSERTING USERTYPE DETAILS 
@app.route('/addtype', methods=['POST'])
def addRole(id=None):
    try:
        json = request.json
        type = json['type']
        userObj = Usertype(id, type)
        if type and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO usertype(type) VALUES( %s)"
            bindData = userObj.type 
            cursor.execute(sqlQuery,bindData)
            conn.commit()
            response = jsonify('User added successfully')
            response.status_code = 200
            return response
        else:
            return "something went wrong" 
    except Exception as e:
        print(e)
        return 'Exception'
# REGISTER
@app.route('/register', methods=['POST'])
def register():
    json = request.json
    fullname= json['fullname']
    username = json['username']
    password = json['password']
    type =json['type']
    registerbook= Register(fullname,username,password)
    if fullname and username and password and type and request.method == 'POST':
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)  
        query= "SELECT * FROM register WHERE username= '%s'" % (username)
        data=cursor.execute(query)
        print(data)
        if data>0:
            conn.commit()
            response = jsonify('User already Exsist!!')
            response.status_code = 200
            return response
        else:   
            sqlQuery = "INSERT INTO register(fullname,username,password,category,type) VALUES(%s, %s, %s,%s)"
            bindData = (registerbook.fullname,registerbook.username,registerbook.password,registerbook.type)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
    else:
        return showMessage()
    
# CREATING CATEGORY DETAILS
@app.route('/category', methods=['POST'])
def addCategory(categoryid=None):
    try:
        json = request.json
        category=json['category']
        categoryobj = Category(categoryid, category)
        if category and request.method =='POST':
            sqlQuery = "INSERT INTO category(category) VALUES(%s)"
            bindData = categoryobj.category
            connect_and_commit(sqlQuery, bindData)
            respone = jsonify('Category details added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'
# DELETING THE CATEGORY DETAILS
@app.route('/category/<categoryid>', methods=['DELETE'])
def deleteCategory(categoryid):
    try:
        sqlQuery = "DELETE FROM category WHERE categoryid =%s"
        data = (categoryid,)
        connect_and_commit(sqlQuery, data)
        response = jsonify('Category Details deleted successfully!')
        response.status_code = 200
        return response
    except Exception as e:
        print(e)
        response = jsonify('Error Occured while deleting the category')
        response.status_code = 500
        return response
#INSERTING BOOK DETAILS
@app.route('/book', methods=['POST'])
def addBook(isbn=None):
    try:
        json = request.json
        bookname= json['bookname'] 
        author = json['author']
        category = json['category']
        price = json['price']
        bookObj = Book(bookname, author, category, price)
        if bookname and author and category and price and request.method =='POST':
            sqlQuery = "INSERT INTO book(bookname, author, category, price) VALUES(%s, %s, %s, %s)"
            bindData = (bookObj.bookname, bookObj.author, bookObj.category, bookObj.price)
            connect_and_commit(sqlQuery, bindData)
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
        _json = request.json
        print(_json)
        _bookname = _json['bookname']
        _author= _json['author']
        _category = _json['category']
        _price = _json['price']
        book= Book(_bookname, _author, _category, _price)
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
    except Exception as e:
        print(e)
        return 'ERROR'
# DELETING BOOK DETAILS
@app.route('/book/<isbn>', methods=['DELETE'])
def deleteBook(isbn):
    try:
        conn = mydb.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM book WHERE isbn =%s",(isbn))
        conn.commit()
        respone = jsonify('Book Details deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
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


    
