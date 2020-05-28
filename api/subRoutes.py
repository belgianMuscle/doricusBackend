from flask import Blueprint, jsonify

sub_api = Blueprint('sub_api', __name__)

@sub_api.route("/sub")
def subApi():
    return jsonify({
      'success':True,
      'content':'Welcome to the Sub API'
    })