import pymysql
import json
from config import mydb
from flask import jsonify
from flask import flash, request
from app import app
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_cors import cross_origin



@app.route('/get', methods=['GET'])
def Get():
    return 'haii'

@app.route('/register', methods=['POST'])
def register():
    
        json = request.json
        print(json)
        fullname= json['fullname']
        username = json['username']
        email= json['email']
        password = json['password']
      
        if fullname and  username and email and password and request.method == 'POST':
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
                 sqlQuery = "INSERT INTO register(fullname,username,email,password) VALUES(%s, %s, %s,%s)"
            bindData = (fullname,username,email,password)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
        else:
            return showMessage()
 


@app.route('/login', methods=['POST'])
def login():
    try:
        json = request.json
        print(json)
        username = json['username']
        password = json['password']
        print(username)
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery="SELECT fullname FROM register WHERE username= '%s'  and password='%s'" % (username, password)
            data=cursor.execute(sqlQuery)
            print(data)
            if data==1:
                access_token = create_access_token(identity=username) 
                conn.commit()
                return jsonify(message='Login Successful', access_token=access_token),200
                 
                
            else:
                conn.commit()
                return jsonify('Bad email or Password... Access Denied!'), 401
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'
    # finally:
    #     cursor.close()
    #     conn.close()

@app.route('/insert', methods=['POST'])
def add_book():
    try:
        json = request.json
        book_name= json['book_name']
        isbn = json['isbn']
        author = json['author']
        category = json['category']
        prize = json['prize']
        if book_name and isbn and author and category and prize and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery = "INSERT INTO book(book_name ,isbn, author, category,prize) VALUES(%s, %s, %s, %s,%s)"
            bindData = (book_name , isbn, author, category,prize)
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
    # finally:
    #     cursor.close()
    #     conn.close()

@app.route('/books', methods =['GET'])
def book():
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT book_name ,isbn, author, category,prize FROM book")
        empRows = cursor.fetchall()
        respone = jsonify(empRows)
        respone.status_code = 200
        return respone
    except Exception as e: 
        print(e)
    finally:
        cursor.close() 
        conn.close() 

@app.route('/bookk/<isbn>', methods=['GET'])
def book_details(isbn):
    try:
        conn = mydb.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT book_name ,isbn, author, category,prize FROM book WHERE isbn =%s", (isbn))
        empRow = cursor.fetchone()
        respone = jsonify(empRow)
        respone.status_code = 200
        return respone
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/update/<isbn>', methods=['PUT'])
def update_book(isbn):
    try:
        _json = request.json
        print(_json)
        _book_name = _json['book_name']
        _isbn = _json['isbn']
        _author= _json['author']
        _category = _json['category']
        _prize = _json['prize']
        if  _book_name and _isbn and _author and _category and  _prize  and request.method  == 'PUT':           
            sqlQuery = ("UPDATE book SET book_name= %s, author= %s, category= %s, prize= %s WHERE isbn=%s")
            bindData = ( _book_name , _author, _category,_prize, _isbn )
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
    # finally:
    #     cursor.close()
    #     conn.close() 


@app.route('/delete/<isbn>', methods=['DELETE'])
def delete_book(isbn):
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

@app.errorhandler(404)
def showMessage(error=None):
    message = {
        'status': 404,
        'message': 'Record not found: ' + request.url,
    }
    respone = jsonify(message)
    respone.status_code = 404
    return respone

if __name__ == "__main__":
    app.run()