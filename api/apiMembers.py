import http.client
import json
from flask import Blueprint, jsonify, abort, request
from database.models import Member
from auth.auth import requires_auth, AUTH0_SECRET, AUTH0_DOMAIN, AUTH0_CLIENT, AUTH0_AUDIENCE

members_api = Blueprint('members_api', __name__)


@members_api.route('/members', methods=['GET'])
@requires_auth('get:account')
def get_member(payload):

    # get auth0
    auth_id = payload.get('sub', '')
    # get Member id from JWT
    member = Member.query.filter(Member.auth0_id == auth_id).one_or_none()

    if not member:
        return jsonify({
            'success': False,
            'member': {}
        })

    if not member.auth0_id == auth_id:
        abort(403)

    member = member.long()
    member['permissions'] = payload.get('permissions', [])

    return jsonify({
        'success': True,
        'member': member
    })

@members_api.route('/searc/members', methods=['GET'])
@requires_auth('search:account')
def get_member_by_email(payload):

    email = request.args.get('email')
    if not email:
        abort(404)

    # get Member id from input email
    member = Member.query.filter(Member.email == email).one_or_none()

    if not member:
        abort(404)

    member = member.long()

    return jsonify({
        'success': True,
        'member': member
    })

@members_api.route('/members', methods=['POST'])
@requires_auth('post:account')
def create_member(payload):

    data = request.get_json()

    if not data:
        return jsonify({
            'success': False,
            'message': 'No account data provided'
        })


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

    update_auth_role(member_data['auth0_id'],member_data["type"])

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

    update_auth_role(member.auth0_id,member_data["type"])

    return jsonify({
        'success': True,
        'member': member.long()
    })


def update_auth_role(user_id, role):
    try:
        conn = http.client.HTTPSConnection(AUTH0_DOMAIN)

        payload = '{"client_id":"'+ AUTH0_CLIENT +'","client_secret":"'+ AUTH0_SECRET +'","audience":"'+ AUTH0_AUDIENCE +'","grant_type":"client_credentials"}'

        headers = { 'content-type': "application/json" }
        conn.request("POST", "/oauth/token", payload, headers)

        res = conn.getresponse()
        data = res.read()
        dec_data = json.loads(data.decode("utf-8"))

        client_token = "bearer " + dec_data['access_token']
        headers = { 'content-type': "application/json", 'Authorization':client_token }

        idata = {
            "roles":[
                "rol_v1f1j1bD6wB03ZGC",
                "rol_w0K2WSAOH7ODeNhX",
                "rol_XyfDRM6MLOEvlZS3"
            ]
        }

        idata = json.dumps(idata)

        url = "/api/v2/users/" + user_id + "/roles"
        
        conn.request("DELETE", url, idata, headers)
        res = conn.getresponse()
        data = res.read().decode()

        role_id = ''
        if role=='ARCHITECT':
            role_id = "rol_v1f1j1bD6wB03ZGC"
        elif role=='BUILDER':
            role_id = "rol_w0K2WSAOH7ODeNhX"
        elif role=='CUSTOMER':
            role_id = "rol_XyfDRM6MLOEvlZS3"

        idata = {
            "roles":[
                role_id
            ]
        }
        idata = json.dumps(idata)

        conn.request("POST", url, idata, headers)
        res = conn.getresponse()
        data = res.read().decode()
    except:
        abort(500)
