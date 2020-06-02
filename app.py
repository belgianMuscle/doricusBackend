import os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import setup_db
from api.subRoutes import sub_api
from api.apiProjects import projects_api
from api.apiMembers import members_api

# create and configure the app
app = Flask(__name__)
setup_db(app)

CORS(app)
# CORS Headers
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

@app.route('/')
def welcome_message():
    return jsonify({
    'success':True,
    'content':'Welcome to the API'
    })

app.register_blueprint(sub_api)
app.register_blueprint(projects_api)
app.register_blueprint(members_api)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Resource not found',
        'error':404
    }),404
 
@app.errorhandler(405)
def not_allowed(error):
    return jsonify({
        'success':False,
        'message':'Method not allowed',
        'error':405
    }),405
 
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        'success':False,
        'message':'Resource cannot be processed',
        'error':422
    }),422
 
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        'success':False,
        'message':'Bad reqeust',
        'error':400
    }),400
 
@app.errorhandler(500)
def request_not_allowed(error):
    return jsonify({
        'success':False,
        'message':'Request not allowed',
        'error':500
    }),500

'''
    error handler for AuthError
    error handler should conform to general task above 
@app.errorhandler(AuthError)
def auth_error_handler(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code
'''
