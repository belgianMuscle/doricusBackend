from flask import Blueprint, jsonify, abort, request
from database.models import Member
from auth.auth import requires_auth

members_api = Blueprint('members_api', __name__)

@members_api.route('/members', methods=['GET'])
@requires_auth('get:account')
def get_member(payload):

    #get auth0
    auth_id = payload.get('sub', '')
    #get Member id from JWT
    member = Member.query.filter(Member.auth0_id == auth_id).one_or_none()

    if not member:
        abort(404)

    if not member.auth0_id == auth_id:
        abort(403)

    member = member.long()
    member['permissions'] = payload.get('permissions',[])

    return jsonify({
        'success': True,
        'member': member
    })


@members_api.route('/members', methods=['POST'])
@requires_auth('post:account')
def create_member(payload):

    data = request.get_json()
    member_data = data.get('member')

    if not member_data:
        return jsonify({
            'success': False,
            'message': 'No account data provided'
        })

    member_data['auth0_id'] = payload.get('sub', '')
    if not member_data['auth0_id']:
        return jsonify({
            'success': False,
            'message': 'No valid authentication credential found'
        })

    member = Member(**member_data)
    member.insert()

    return jsonify({
        'success': True,
        'member': member.long()
    })


@members_api.route('/members/<member_id>', methods=['PATCH'])
@requires_auth('patch:account')
def update_member(payload, member_id):

    member = Member.query.get(member_id)
    if not member:
        abort(404)

    if not member.auth0_id == payload.get('sub', ''):
        abort(403)

    data = request.get_json()
    member_data = data.get('member')

    if not member_data:
        return jsonify({
            'success': False,
            'message': 'No account data provided'
        })

    member.set_data(member_data)
    member.update()

    return jsonify({
        'success': True,
        'member': member.long()
    })
