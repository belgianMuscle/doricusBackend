from flask import Blueprint, jsonify, abort
from database.models import Project, Topic, Member
from api.localpayload import payload

project_members_api = Blueprint('project_members_api', __name__)


@project_members_api.route("/project_member",methods=['GET'])
def get_member():
    
  return jsonify({
        'success':True,
        'route':'Get all'
      })
    
@project_members_api.route('/project_member/<member_id>',methods=['GET'])
def get_member_by_id(member_id):

  return jsonify({
        'success':True,
        '':'Get single'
      })

@project_members_api.route('/project_member',methods=['POST'])
def create_project():

  return jsonify({
        'success':True,
        'route':'Create'
      })

@project_members_api.route('/project_member/<member_id>',methods=['PATCH'])
def update_project(member_id):

  return jsonify({
        'success':True,
        'route':'Update'
      })

@project_members_api.route('/project_member/<member_id>',methods=['DELETE'])
def delete_project(member_id):
    member = Member.query.get(member_id)
    if not member:
        abort(404)

    member.delete()   

    return jsonify({
        'success': True,
        'member_id': member_id
    })