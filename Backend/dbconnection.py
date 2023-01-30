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

def connect_and_commit(query, data=None):
    conn = mydb.connect()
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, data)
    conn.commit()
    cursor.close()
    conn.close()
   
# def connect_and_commit(query, data=None):
#     conn = mydb.connect()
#     cursor = conn.cursor(pymysql.cursors.DictCursor)
#     cursor.execute(query, data)
#     conn.commit()
#     cursor.close()
#     close_connection(conn)

# def close_connection(conn):
#     conn.close()
