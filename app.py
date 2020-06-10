import os
import logging

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from database.models import setup_db

from auth.auth import AuthError

from api.apiProjects import projects_api
from api.apiMembers import members_api
from api.apiTopics import topics_api
from api.apiTopicComments import topiccomments_api

FRONTEND_ORIGIN = os.environ.get('FRONTEND_ORIGIN','')
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'DEBUG')

def _logger():
    '''
    Setup logger format, level, and handler.

    RETURNS: log object
    '''
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    log = logging.getLogger(__name__)
    log.setLevel(LOG_LEVEL)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    log.addHandler(stream_handler)
    return log


LOG = _logger()
LOG.debug("Starting with log level: %s" % LOG_LEVEL )

# create and configure the app
app = Flask(__name__)
setup_db(app)

CORS(app)
# CORS Headers
@app.after_request
def after_request(response):
    white_origin= ['https://doricus.herokuapp.com','doricus-backend.herokuapp.com','https://doricus-backend.herokuapp.com','http://localhost:3000','http://localhost:5000','http://127.0.0.1:5050','localhost']
    #if request.headers['Origin'] in white_origin:
    try:
        origin = request.headers['Origin']
    except:
        origin = request.headers['Host']

    print('Origin: {}'.format(origin))

    if origin in white_origin:
        response.headers['Access-Control-Allow-Origin'] = origin 
        response.headers['Access-Control-Allow-Methods'] = 'GET,POST,DELETE,PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type,Authorization,true'
    return response

@app.route('/')
def welcome_message():
    
    return jsonify({
    'success':True,
    'content':'Welcome to the API'
    })

app.register_blueprint(projects_api)
app.register_blueprint(members_api)
app.register_blueprint(topics_api)
app.register_blueprint(topiccomments_api)

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
    print('General Bad Request')
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
'''
@app.errorhandler(AuthError)
def auth_error_handler(error):
    print('Auth issue')
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code