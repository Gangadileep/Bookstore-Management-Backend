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

# USER REGISTRATION
@app.route('/register', methods=['POST'])
def register():
    json = request.json
    print(json)
    fullname= json['fullname']
    username = json['username']
    email= json['email']
    password = json['password']
    category ='user'
    if fullname and  username and email and password and category and request.method == 'POST':
        query= "SELECT * FROM register WHERE username= '%s'" % (username)
        data = execute_query(query)
        print(data)
        if data>0:
            response = jsonify('User already Exsist!!')
            response.status_code = 200
            return response
        else:   
            sqlQuery = "INSERT INTO register(fullname,username,email,password,category) VALUES(%s,%s, %s, %s,%s)"
            bindData = (fullname,username,email,password,category)
            db_commit_connection(sqlQuery, bindData)
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
    else:
        return showMessage()

#ADMIN AND USER LOGIN 
@app.route('/login', methods=['POST'])
def login():
    json = request.json
    if not json.get('username') or not json.get('password'):
        return handle_credentials()
    try:
        username = json['username']
        password = json['password']
        if request.method == 'POST':
            sqlQuery = "SELECT * FROM register WHERE username= '%s' and password='%s'" % (username, password)
            cursor = execute_query(sqlQuery)
            row = cursor.fetchone() 
            category = row.get('category')       
            if cursor.rowcount == 1:
                access_token = create_access_token(identity=username) 
                return jsonify(message='Login Successful', access_token=access_token ,category=category),200
            else:
                return jsonify('Bad email or Password... Access Denied!'), 401
        else:
            return showMessage()          
    except Exception as e:
        print(e)
        return jsonify(message='Error Occured'), 500

# INSERTING THE BOOK DETAILS
@app.route('/insert', methods=['POST'])
def add_book():
    try:
        json = request.json
        bookname= json['bookname']
        isbn = json['isbn'] 
        author = json['author']
        category = json['category']
        price = json['price']
        if bookname and isbn and author and category and price and request.method =='POST':
            sqlQuery = "INSERT INTO book(bookname ,isbn, author,category,price) VALUES(%s, %s, %s, %s,%s)"
            bindData = (bookname,isbn, author,category,price)
            db_commit_connection(sqlQuery, bindData)
            respone = jsonify('Book details added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'

#VIEWING THE BOOK DETAILS 
@app.route('/books', methods =['GET'])
def book():
    try:
        sqlQuery="SELECT bookname ,isbn, author, category, price FROM book"
        cursor = execute_query(sqlQuery)
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e: 
        print(e)   

#VIEWING THE PARTICULAR BOOK DETAILS BY ISBN
@app.route('/bookk/<isbn>', methods=['GET'])
def book_details(isbn):
    try:
        sqlQuery=("SELECT bookname ,isbn, author, category, price FROM book WHERE isbn =%s", (isbn))
        cursor = execute_query(sqlQuery)
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)

# UPDATING THE BOOK DETAILS
@app.route('/update/<isbn>', methods=['PUT'])
def update_book(isbn):
    try:
        newjson = request.json
        newbookname = newjson['bookname']
        newisbn = newjson['isbn']
        newauthor= newjson['author']
        newcategory = newjson['category']
        newprice = newjson['price']
        if  newbookname and newisbn and newauthor and newcategory and  newprice  and request.method == 'PUT':           
            sqlQuery = ("UPDATE book SET bookname= %s, author= %s, category= %s, price= %s WHERE isbn=%s")
            bindData = ( newbookname, newauthor, newcategory, newprice, newisbn )
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

# DELETING BOOK DETAILS 
@app.route('/delete/<isbn>', methods=['DELETE'])
def delete_book(isbn):
    try:
        sqlQuery = ("DELETE FROM book WHERE isbn =%s",(isbn))
        cursor = execute_query(sqlQuery)
        respone = jsonify('Book Details deleted successfully!')
        respone.status_code = 200
        return respone
    except Exception as e:
        return 'Exception'

#FUNCTION FOR DATABASE CONNECTION    
def execute_query(query):
    conn = mydb.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query)
    conn.commit()
    conn.close()
    return cursor

#FUNCTION FOR DATABASE CONNECTION 
def db_commit_connection(query, data=None):
    conn = pymysql.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    if data:
        cursor.execute(query, data)
    else:
        cursor.execute(query)
    conn.commit()
    cursor.close()
    conn.close()  

#SHOWING ERROR
@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

#ERROR HANDLING
@app.errorhandler(400)
def handle_credentials():
    message ={
        "status": 400,
        "message" :"Missing Username or password"
    }
    return jsonify(message)

# RUN SERVER
if __name__ == "__main__":
    app.run()


        
            
