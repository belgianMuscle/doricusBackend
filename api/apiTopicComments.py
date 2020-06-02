from flask import Blueprint, jsonify, abort, request
from database.models import Project, Topic, Member, TopicComment
from api.localpayload import payload
from sqlalchemy.orm import lazyload

topiccomments_api = Blueprint('topiccomments_api', __name__)

@topiccomments_api.route('/projects/<project_id>/topics/<topic_id>/comments',methods=['POST'])
def create_comment(project_id,topic_id):

  data = request.get_json()
  comment_data = data.get('comment')

  if not comment_data:
        return jsonify({
        'success':False,
        'message':'No comment data provided'
      })

  topic = Topic.query.get(topic_id)
  if not topic:
        abort(403)

  member = Member.query.options(lazyload(Member.projects)).filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()
  
  if not member:
        abort(403)

  if not project_id in [ p.id for p in member.projects ]:
        abort(403)

  comment_data.topic_id = topic_id
  comment_data.member_id = member.id

  comment = TopicComment(**comment_data)
  comment.insert()

  return jsonify({
        'success':True,
        'comment':comment
      })