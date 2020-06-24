from flask import Blueprint, jsonify, abort, request
from database.models import Project, Topic, Member, ProjectMember, getCurrentTime
from auth.auth import requires_auth
from sqlalchemy.orm import lazyload

projects_api = Blueprint('projects_api', __name__)


@projects_api.route("/projects", methods=['GET'])
@requires_auth('get:projects')
def get_projects(payload):
    #get auth0
    auth_id = payload.get('sub', '')
    #get member from auth    
    try:
        member = Member.query.filter(Member.auth0_id == auth_id).one_or_none()
    except:
        abort(403)
        

    if member:
        member.projects = Project.query.with_parent(member).all()
        openProjects = [p.long() for p in member.projects if p.act_end_date > getCurrentTime()]
        closedProjects = [p.long() for p in member.projects if p.act_end_date <= getCurrentTime()]

        return jsonify({
            'success': True,
            'openProjects': openProjects,
            'closedProjects': closedProjects,
            'openProjectCount': len(openProjects),
            'closedProjectCount': len(closedProjects)

        })
    else:
        abort(404)


@projects_api.route('/projects/<project_id>', methods=['GET'])
@requires_auth('get:projects')
def get_project(payload, project_id):

    try:
        member = Member.query.filter(
                Member.auth0_id == payload.get('sub', '')).one_or_none()
    except:
        abort(403)

    project = Project.query.options(lazyload(Project.members)).get(project_id)

    if not project:
        abort(404)

    # verify member is allowed to pick this
    # Maybe I can change this to a nested call instead...
    if not member.id in [ m.member_id for m in project.members]:
        abort(403)

    topics = Topic.query.options(lazyload(Topic.comments)).with_parent(project).all()

    output_project = project.long()
    output_project['topics'] = [p.long() for p in topics]

    return jsonify({
        'success': True,
        'project': output_project
    })


@projects_api.route('/projects', methods=['POST'])
@requires_auth('post:projects')
def create_project(payload):

    try:
        member = Member.query.filter(
                Member.auth0_id == payload.get('sub', '')).one_or_none()
    except:
        abort(403)

    if not member:
        abort(403)

    data = request.get_json()
    project_data = data['project']

    if not project_data:
        abort(400)

    project = Project(member.id)
    project.set_data(project_data)
    project.insert()

    pm = ProjectMember(project.id,member.id)
    pm.insert()

    return jsonify({
        'success': True,
        'project': project.long()
    })


@projects_api.route('/projects/<project_id>', methods=['PATCH'])
@requires_auth('patch:projects')
def update_project(payload, project_id):
    data = request.get_json()
    project_data = data.get('project')

    try:
        member = Member.query.filter(
                Member.auth0_id == payload.get('sub', '')).one_or_none()
    except:
        abort(403)

    if not member:
        abort(403)

    project = Project.query.get(project_id)

    if not project:
        abort(404)
    if not project.member_id == member.id:
        abort(403)

    project.set_data(project_data)
    project.update()

    return jsonify({
        'success': True,
        'project': project.long()
    })


@projects_api.route('/projects/<project_id>', methods=['DELETE'])
@requires_auth('delete:projects')
def delete_project(payload, project_id):

    try:
        member = Member.query.filter(
                Member.auth0_id == payload.get('sub', '')).one_or_none()
    except:
        abort(403)

    if not member:
        abort(403)

    project = Project.query.get(project_id)

    if not project:
        abort(404)
    if not project.member_id == member.id:
        abort(403)
    
    project.delete()    

    return jsonify({
        'success': True,
        'project_id': project_id
    })
