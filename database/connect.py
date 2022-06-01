# -*- coding: UTF-8 -*-
import sys
import redis
from typing import NoReturn
from utils.const import DBConst


class BaseConnect(object):

    """
    Manages TCP communication to and from a database server.
    """

    def __init__(self, host='localhost', port=None,
                 username=None, password=None, database=None):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def _on_connect(self, component=None) -> bool or NoReturn:
        """Connection parameter check"""
        _default_ports = {
            DBConst.MYSQL_COMPONENT: DBConst.MYSQL_LISTENING_PORT,
            DBConst.PGSQL_COMPONENT: DBConst.PGSQL_LISTENING_PORT,
            DBConst.REDIS_COMPONENT: DBConst.REDIS_LISTENING_PORT
        }
        self._component = component

        if self.host is None:
            self.abort(keyword="host")

        if self.password is None:
            self.abort(keyword="password")

        if self.port is None:
            self.port = _default_ports.get(component.lower(), None)

        if not isinstance(self.port, int):
            self.abort(keyword="port")

        if component.lower() != DBConst.REDIS_COMPONENT:
            if not self.username:
                self.abort(keyword="username")
            if not self.database:
                self.abort(keyword="database")
        return True

    def abort(self, keyword=None) -> NoReturn:
        _warning = f"\nPlease check {self._component.upper()} connection parameters, '?' is required."
        del self._component
        if keyword is None:
            keyword = "?type"
        sys.exit(_warning.replace("?", keyword))


class RedisConn(BaseConnect):

    """
    Abstract class for implementing Redis connections.
    """

    # Default redis server listening port number.
    DEFALUT_REDIS_PORT: int = DBConst.REDIS_LISTENING_PORT

    # Maximum number of connections for redis.
    MAX_CONNECTIONS: int = DBConst.REDIS_MAX_CONNS_LIMIT

    def __init__(self, ipaddr='127.0.0.1', port=None, password=None, component=None):
        self.port = port
        if self.port is None:
            if isinstance(self.__class__.DEFALUT_REDIS_PORT, int):
                self.port = self.__class__.DEFALUT_REDIS_PORT
        # print(self.__class__.__base__)
        BaseConnect.__init__(
            self,
            host=ipaddr,
            port=self.port,
            password=password
        )
        self._on_connect(component=component)

    def __enter__(self):
        """
        Create a connection pool and establish
        an active connection.
        """
        try:
            self.pool = redis.ConnectionPool(
                host=self.host,
                port=self.port,
                password=self.password,
                max_connections=self.MAX_CONNECTIONS
            )
            # The result retrieved by redis is byte type by default,
            # we can set 'decode_responses=True' to string
            self.conn = redis.Redis(
                connection_pool=self.pool,
                decode_responses=True
            )
            test = self.ping_pong
            if test.upper() != "PONG":
                _warning = "\nNot connected, please check network or service."
                sys.exit(_warning)
        except Exception as e:
            if self.conn:
                self.conn.close()
            _warning = f"\nIP: {self.host}, PASSWD: {'*' * len(self.password)}\nREASON: {str(e)}"
            raise Exception(_warning)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Close a connection and pool.
        """
        if self.conn:
            self.conn.close()
        return None

    @property
    def ping_pong(self) -> str:
        flag = self.conn.ping()
        return "PONG" if flag else ""


