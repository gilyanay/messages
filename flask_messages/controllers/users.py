from flask import Blueprint, request, make_response, jsonify
from sqlalchemy.orm import Session
from flask_messages.repositories import mysql
from models.users import User
import json

users_bp = Blueprint("users", __name__)


@users_bp.route("/login", methods=["POST"])
def login():
    item: User = User(**json.loads(request.data))
    with mysql.session_scope() as s:
        s: Session
        user = s.query(User).filter(User.user_name == item.user_name, User.password == item.password).first()
        auth_token = user.encode_auth_token(user.id)
    try:
        if auth_token:
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'auth_token':  auth_token
            }
            return make_response(jsonify(response_object)), 200
    except Exception as e:
        print(e)
        response_object = {
            'status': 'fail',
            'message': 'Try again'
        }
        return make_response(jsonify(response_object)), 500


def get_user_id(user_name: int) -> int:
    with mysql.session_scope() as s:
        s: Session
        user_id: int = s.query(User.id).filter(User.user_name == user_name).first()
        if user_id:
            return user_id.id
