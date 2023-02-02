import jwt
from flask import jsonify
from flask import request
from app import app
from functools import wraps

def check_for_token(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        access_token = request.headers.get('Authorization')
        
        access_token = access_token.replace('Bearer ', '')
        # print(access_token)
        if not access_token:
            return jsonify({'message': 'Missing token!'}), 403
        try:
            jwt.decode(access_token, app.config['JWT_SECRET_KEY'], algorithms='HS256')
            print(access_token) 
        except:
            return jsonify({'message': 'Invalid token!'}), 403  
        return func(*args, **kwargs)
    return wrapped
