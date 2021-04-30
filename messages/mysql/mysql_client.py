import logging
import os
from contextlib import contextmanager
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

ECHO_SQL_LOGS = os.getenv("ECHO_SQL_LOGS") == "1"
SqlTableDeclarativeBase = declarative_base()


class MySqlClient:

    def __init__(self, connection_string: str):
        self.__engine = create_engine(
            connection_string, echo=ECHO_SQL_LOGS, pool_size=20, pool_recycle=1200, pool_timeout=3600,
        )
        self.__session_maker = sessionmaker(bind=self.__engine)
        self.log = logging.getLogger(__name__)



    @contextmanager
    def session_scope(self):
        """Provide a transactional scope around a series of operations."""
        session = self.__session_maker()
        session: Session
        try:
            self.log.debug(f"enter {session=}")
            yield session
            session.commit()
        except Exception as error:
            self.log.exception(error)
            session.rollback()
            raise error
        finally:
            self.log.debug(f"closing {session=}")
            session.close()

    @classmethod
    def get_mysql_client(cls, user: str, host: str, scheme: str, password: str, port="3306") -> "MySqlClient":
        connection_string = f"mysql+pymysql://{user}:{password}@{host}:{port}/{scheme}?charset=utf8mb4"
        return cls(connection_string)
