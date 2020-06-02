from flask import Blueprint, jsonify, abort, request
from database.models import Member
from api.localpayload import payload

members_api = Blueprint('members_api', __name__)

@members_api.route('/members/<member_id>', methods=['GET'])
def get_member(member_id):

    member = Member.query.get(member_id)

    if not member:
        abort(404)

    if not member.auth0_id == payload.get('sub', ''):
        abort(403)

    return jsonify({
        'success': True,
        'member': member.long()
    })


@members_api.route('/members', methods=['POST'])
def create_member():

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
def update_member(member_id):

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
