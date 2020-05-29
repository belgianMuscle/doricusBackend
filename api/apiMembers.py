from flask import Blueprint, jsonify, abort
from database.models import Project, Topic, Member
from api.localpayload import payload

members_api = Blueprint('members_api', __name__)


@members_api.route("/members",methods=['GET'])
def get_members():
    
  return jsonify({
        'success':True,
        'route':'Get all'
      })
    
@members_api.route('/members/<member_id>',methods=['GET'])
def get_member(project_id):

  return jsonify({
        'success':True,
        'route':'Get single'
      })

@members_api.route('/members',methods=['POST'])
def create_member():

  return jsonify({
        'success':True,
        'route':'Create'
      })

@members_api.route('/members/<member_id>',methods=['PATCH'])
def update_member(project_id):

  return jsonify({
        'success':True,
        'route':'Update'
      })

@members_api.route('/members/<member_id>',methods=['DELETE'])
def delete_member(project_id):

  return jsonify({
        'success':True,
        'route':'Delete'
      })