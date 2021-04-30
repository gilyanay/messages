
from sqlalchemy import Column, Integer, String, DateTime, Boolean

from mysql import SqlTableDeclarativeBase


class Message(SqlTableDeclarativeBase):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, autoincrement=True)
    message = Column(String(100), nullable=False)
    creation_date = Column(DateTime, nullable=False, default=1)
    sender_id = Column(Integer, nullable=False)
    receiver_id = Column(Integer,nullable=False)
    subject = Column(String(45), nullable=False)
    is_read = Column(Boolean,  nullable=False, default=0)

    def _str_(self):
        return f"message {self.subject} id {self.id}"
