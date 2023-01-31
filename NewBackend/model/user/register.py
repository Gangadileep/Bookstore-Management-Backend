import pymysql
import bcrypt
from config import mydb
from flask import jsonify
from flask import  request
from validate import validate_register_data
from app import app
from flask_jwt_extended import create_access_token
from flask_cors import cross_origin
from classes import Usertype, Register

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
def register(id=None):
    json = request.json
    fullname= json['fullname']
    username = json['username']
    password = json['password']
    type ='2'
    validation_error = validate_register_data(fullname, username, password)
    if validation_error:
        return validation_error
    hashed_password = hash_password(password)
    registerbook= Register(id,fullname,username,hashed_password,type)
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
            sqlQuery = "INSERT INTO register(fullname,username,password,type) VALUES(%s, %s, %s,%s)"
            bindData = (registerbook.fullname,registerbook.username,registerbook.password,registerbook.type)
            cursor.execute(sqlQuery, bindData)
            conn.commit()
            respone = jsonify('User added successfully!')
            respone.status_code = 200
            return respone
    else:
        return showMessage()

# LOGIN 
@app.route('/login', methods=['POST'])
def login():
    try:
        json = request.json
        username = json['username']
        password = json['password']
        if username and password and request.method == 'POST':
            conn = mydb.connect()
            cursor = conn.cursor(pymysql.cursors.DictCursor)
            sqlQuery="SELECT * FROM register WHERE username= '%s'" % (username)
            data=cursor.execute(sqlQuery)
            if data==1:
                row = cursor.fetchone() 
                stored_hashed_password = row.get('password')
                type = row.get('type')              
                if verify_password(password, stored_hashed_password):
                    access_token = create_access_token(identity=username) 
                    conn.commit()
                    return jsonify(message='Login Successful', access_token=access_token ,type=type),200
                else:
                    conn.commit()
                    return jsonify('Bad email or Password... Access Denied!'), 401
            else:
                conn.commit()
                return jsonify('Bad email or Password... Access Denied!'), 401
        else:
            return showMessage()
    except Exception as e:
        print(e)
        return 'Exception'

#HASHING PASSWORD
def hash_password(password):
    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password, salt)
    print(hashed_password.decode("utf-8"))
    return hashed_password.decode('utf-8')

#VERIFYING THE PASSWORD
def verify_password( password,hashed_password):
    password = password.encode('utf-8')
    hashed_password = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password, hashed_password)
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