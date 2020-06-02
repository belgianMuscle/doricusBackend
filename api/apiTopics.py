from flask import Blueprint, jsonify, abort, request
from database.models import Project, Topic, Member
from api.localpayload import payload
from sqlalchemy.orm import lazyload

topics_api = Blueprint('topics_api', __name__)
    
@topics_api.route('/projects/<project_id>/topics/<topic_id>',methods=['GET'])
def get_topic(project_id,topic_id):

  member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()
  
  if not member:
        abort(403)
  
  project = Project.query.options(lazyload(Project.members)).get(project_id)
  if not project:
        abort(404)
  
  if not member.id in [ m.id for m in project.members ]:
        abort(403)

  topic = Topic.query.options(lazyload(Topic.comments)).get(topic_id)

  return jsonify({
        'success':True,
        'topic':topic.long()
      })

@topics_api.route('/projects/<project_id>/topics',methods=['POST'])
def create_topic(project_id):

  data = request.get_json()
  topic_data = data.get('topic')

  if not topic_data:
        abort(405)

  member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()
  
  if not member:
        abort(403)
  
  project = Project.query.options(lazyload(Project.members)).get(project_id)
  if not project:
        abort(404)
  
  if not member.id in [ m.id for m in project.members ]:
        abort(403)

  topic_data['project_id'] = project.id
  topic_data['member_id'] = member.id

  topic = Topic(**topic_data)
  topic.insert()

  return jsonify({
        'success':True,
        'topic':topic.long()
      })

@topics_api.route('/topics/<topic_id>',methods=['PATCH'])
def update_topic_visibility(topic_id):
  #This only updates the visibility for now

  data = request.get_json()
  topic_data = data.get('topic')

  topic = Topic.query.get(topic_id)

  member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()

  if not member.id == topic.member_id:
        abort(403)

  topic.visibility = topic_data.get('visibility','CLOSED')

  topic.update()

  return jsonify({
        'success':True,
        'topic':topic.long()
      })

@topics_api.route('/topics/<topic_id>',methods=['DELETE'])
def delete_topic(topic_id):

  topic = Topic.query.get(topic_id)

  member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()

  if not member.id == topic.member_id:
        abort(403)

  topic.delete()

  return jsonify({
        'success':True,
        'topic_id':topic_id
      })