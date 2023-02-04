from app import app
from flask import request
from dbconnection import connect_and_commit
from flask import jsonify
from classes import Category
from auth import check_for_token
from log import logger

# CREATING CATEGORY DETAILS
@app.route('/category', methods=['POST'])
@check_for_token
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
    except KeyError as e:
        logger.error(f"KeyError: {e}")
        return jsonify({'error': 'A required key is missing from the request'})

# DELETING THE CATEGORY DETAILS
@app.route('/category/<categoryid>', methods=['DELETE'])
@check_for_token
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
