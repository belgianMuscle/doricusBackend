from flask import Blueprint, jsonify, abort
from database.models import Project, Topic, Member
from api.localpayload import payload

project_members_api = Blueprint('project_members_api', __name__)


@project_members_api.route("/project_member",methods=['GET'])
def get_projects():
    
  return jsonify({
        'success':True,
        'route':'Get all'
      })
    
@project_members_api.route('/project_member/<project_id>',methods=['GET'])
def get_project(project_id):

  return jsonify({
        'success':True,
        'route':'Get single'
      })

@project_members_api.route('/project_member',methods=['POST'])
def create_project():

  return jsonify({
        'success':True,
        'route':'Create'
      })

@project_members_api.route('/project_member/<project_id>',methods=['PATCH'])
def update_project(project_id):

  return jsonify({
        'success':True,
        'route':'Update'
      })

@project_members_api.route('/project_member/<project_id>',methods=['DELETE'])
def delete_project(project_id):

  return jsonify({
        'success':True,
        'route':'Delete'
      })