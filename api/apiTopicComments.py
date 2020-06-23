from flask import Blueprint, jsonify, abort, request
from database.models import Project, Topic, Member, TopicComment, getCurrentTime
from auth.auth import requires_auth
from sqlalchemy.orm import lazyload

topiccomments_api = Blueprint('topiccomments_api', __name__)


@topiccomments_api.route('/projects/<project_id>/topics/<topic_id>/comments', methods=['POST'])
@requires_auth('post:comments')
def create_comment(payload, project_id, topic_id):

    data = request.get_json()
    comment_data = data.get('comment')

    if not comment_data:
        return jsonify({
            'success': False,
            'message': 'No comment data provided'
        })

    topic = Topic.query.get(topic_id)
    if not topic:
        abort(404)

    member = Member.query.options(lazyload(Member.projects)).filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()

    if not member:
        abort(403)

    project = Project.query.options(lazyload(Project.members)).get(project_id)

    if not project:
        abort(404)
    
    if not member.id in [m.member_id for m in project.members]:
        abort(403)

    comment_data['topic_id'] = topic_id
    comment_data['member_id'] = member.id
    comment_data['timestamp'] = getCurrentTime()

    comment = TopicComment(**comment_data)
    comment.insert()

    return jsonify({
        'success': True,
        'comment': comment.long()
    })
