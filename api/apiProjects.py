from flask import Blueprint, jsonify, abort, request
from database.models import Project, Topic, Member, ProjectMember
from api.localpayload import payload
from sqlalchemy.orm import lazyload

projects_api = Blueprint('projects_api', __name__)


@projects_api.route("/projects", methods=['GET'])
def get_projects():

    member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()

    if member:
        member.projects = Project.query.with_parent(member).all()
        projects = [p.long() for p in member.projects]
        return jsonify({
            'success': True,
            'projects': projects
        })
    else:
        abort(404)


@projects_api.route('/projects/<project_id>', methods=['GET'])
def get_project(project_id):

    member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()
    project = Project.query.options(lazyload(Project.members)).get(project_id)

    # verify member is allowed to pick this
    # Maybe I can change this to a nested call instead...
    if not member.id in [ m.id for m in project.members]:
        abort(404)

    return jsonify({
        'success': True,
        'project': project.long()
    })


@projects_api.route('/projects', methods=['POST'])
def create_project():

    member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()
    if not member:
        abort(403)

    data = request.get_json()
    project_data = data['project']

    project = Project(member.id)
    project.set_data(project_data)
    project.insert()

    return jsonify({
        'success': True,
        'project': project.long()
    })


@projects_api.route('/projects/<project_id>', methods=['PATCH'])
def update_project(project_id):
    data = request.get_json()
    project_data = data.get('project')

    member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()
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
def delete_project(project_id):

    member = Member.query.filter(
        Member.auth0_id == payload.get('sub', '')).one_or_none()
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
