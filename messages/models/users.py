from datetime import datetime, timedelta
from sqlalchemy import Column, Integer, String
import config
from mysql import SqlTableDeclarativeBase
import jwt


class User(SqlTableDeclarativeBase):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_name = Column(String(45), nullable=False, unique=True)
    password = Column(String(45), nullable=False)

    def _str_(self):
        return f"user {self.subject} id {self.id}"

    @staticmethod
    def encode_auth_token(user_id):
        try:
            payload = {
                'exp': datetime.utcnow() + timedelta(days=1, seconds=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                config.SECRET_KEY,
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        try:
            payload = jwt.decode(auth_token, config.SECRET_KEY, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
