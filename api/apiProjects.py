from flask import Blueprint, jsonify

projects_api = Blueprint('projects_api', __name__)

@projects_api.route("/projects",methods=['GET'])
def get_projects():
    return jsonify({
      'success':True,
      'content':'Welcome to the Projects API'
    })