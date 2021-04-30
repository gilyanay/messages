import logging
import os
from contextlib import contextmanager
from threading import Lock

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

"""
Use the get_mysql_client class method to get new instance of MySqlClient
Each connection string will have a different instance of MySqlClient
do not call _init_ directly 
"""
ECHO_SQL_LOGS = os.getenv("ECHO_SQL_LOGS") == "1"
SqlTableDeclarativeBase = declarative_base()


class MySqlClient:
    __CLIENT_TO_CONNECTION_STRING: dict = dict()
    __LOCK = Lock()

    def _init_(self, connection_string: str):
        self.__engine = create_engine(
            connection_string, echo=ECHO_SQL_LOGS, pool_size=20, pool_recycle=1200, pool_timeout=3600,
        )
        self._session_maker = sessionmaker(bind=self._engine)
        self.log = logging.getLogger(__name__)

    def create_all_tables(self):
        try:
            SqlTableDeclarativeBase.metadata.create_all(self.__engine)
        except Exception as e:
            self.log.exception(e)

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
        return cls(f"mysql+pymysql://{user}:{password}@{host}:{port}/{scheme}?charset=utf8mb4")
