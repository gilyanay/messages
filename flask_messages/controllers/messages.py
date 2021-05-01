import datetime
import json
import logging
from typing import List

from flask import Blueprint, request, make_response, jsonify
from sqlalchemy.orm import Session

from flask_messages.repositories import mysql
from models.messege import Message
from models.users import User
from .users import get_user_id

log = logging.getLogger(__name__)
messages_bp = Blueprint("messages", __name__)


@messages_bp.route("/send", methods=["POST"])
def send():
    req = json.loads(request.data)
    message: Message = Message(
        message=req["message"],
        sender_id=get_payload_from_auth(),
        receiver_id=get_user_id(req["to"]),
        subject=req["subject"],
        creation_date=datetime.datetime.now()

    )
    with mysql.session_scope() as s:
        s: Session
        s.add(message)
        return make_response(200)


@messages_bp.route("/get_all_messages", methods=["GET"])
def get_all_messages():
    user_id = get_payload_from_auth()
    with mysql.session_scope() as s:
        s: Session
        messages = s.query(Message).filter(Message.sender_id == user_id).all()
        return message_response_format(messages)


@messages_bp.route("/get_all_unread_messages", methods=["GET"])
def get_all_unread_messages():
    user_id = get_payload_from_auth()
    with mysql.session_scope() as s:
        s: Session
        messages = s.query(Message).filter(Message.sender_id == user_id, Message.is_read == 0).all()
        return message_response_format(messages)


@messages_bp.route("/read_message/<int:message_id>", methods=["GET"])
def read_message(message_id):
    user_id = get_payload_from_auth()
    with mysql.session_scope() as s:
        s: Session
        message = s.query(Message).filter(Message.sender_id == user_id, Message.id == message_id).first()
        if message:
            message.is_read = 1
            s.commit()
        return message_response_format(message)


@messages_bp.route("/delete_message/<int:message_id>", methods=["DELETE"])
def delete_message(message_id: int):
    user_id = get_payload_from_auth()
    with mysql.session_scope() as s:
        s: Session
        s.query(Message).filter(
            Message.id == message_id
            and (Message.sender_id == user_id or Message.receiver_id == user_id)).delete()


def get_payload_from_auth() -> int:
    auth_token = request.headers.get('Authorization')
    if auth_token:
        user_id: int = User.decode_auth_token(auth_token)
        return user_id


def message_response_format(messages:List[Message]):
    messages_to_send= []
    for message in messages:
        messages_to_send.append(
            {
                "message id": message.id,
                "subject": message.subject,
                "message": message.message
            })
    return jsonify({"messages": messages_to_send})
