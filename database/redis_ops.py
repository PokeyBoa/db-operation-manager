# -*- coding: UTF-8 -*-
import json
import copy
from typing import Dict, List, Tuple
from logger.logger import Console
from database.connect import RedisConn
from utils.base_class import KwargsClass
from utils.const import DBConst, LogLevel
from utils.json_util import AdvancedEncoder


class RedisOps(KwargsClass, RedisConn):

    """
    Abstract class for implementing basic operations
    of the database (Redis) curd.
    """

    # The default cache redis data
    # expiration time is 5 minutes.
    EXPIRE_TIME: int = DBConst.REDIS_EXPIRE_TIME

    # Default international character
    # encoding (utf-8).
    CHAR_ENCODING: str = DBConst.CHARACTER_ENCODING

    def __init__(self, level=2, **kwargs):
        grade = LogLevel().LOG_Level_List
        if isinstance(level, int):
            if 0 < level < len(grade) + 1:
                _level = level
            else:
                _level = 2
            self.console = Console(level=_level)
        else:
            self.console = None

        KwargsClass.__init__(self, **kwargs)
        arglist = self.attributes.get('kwargs')
        for i in arglist:
            if i.lower() in ["ipaddr", "host"]:
                self.ipaddr = eval(f"self.{i}")
            elif i.lower() in ["port"]:
                self.port = int(eval(f"self.{i}"))
            elif i.lower() in ["password", "passwd", "pwd"]:
                self.password = eval(f"self.{i}")
            elif i.lower() in ["component", "techstack", "database", "name"]:
                self.component = eval(f"self.{i}")
        else:
            if "port" not in arglist:
                self.port = None

        RedisConn.__init__(
            self,
            ipaddr=self.ipaddr,
            port=self.port,
            password=self.password,
            component=self.component
        )

    def del_keys(self, keys: Tuple[str]) -> bool:
        """
        Delete redis keys data.
        """
        flag = self.conn.delete(*keys)
        if flag:
            if self.console is not None:
                self.console(f"{self.host} Successfully delete the redis keys.")
            return True
        if self.console is not None:
            self.console(f"{self.host} Failed delete the redis keys.")
        return False

    def set_string(
            self,
            key: str,
            value: str,
            ex=EXPIRE_TIME
    ) -> bool:
        """
        Store redis string type data.
        """
        try:
            self.conn.set(name=key, value=value, ex=ex)
            self.conn.save()
            if self.console is not None:
                self.console(f"{self.host} Successfully set the value of redis key (string).")
            return True
        except:
            if self.console is not None:
                self.console(f"{self.host} Failed to set the value of redis key (string).")
            return False

    def get_string(self, key: str) -> Dict[str, any]:
        """
        View redis string type data.
        """
        result = {}
        data = self.conn.get(name=key)
        if data:
            convert = None
            try:
                # Attempt to convert unknown data type to python type.
                # such as list in string, etc.
                convert = eval(data.decode(self.CHAR_ENCODING))
            except:
                # Use the default string type.
                convert = data.decode(self.CHAR_ENCODING)
            finally:
                result.update({
                    key: convert
                })
        if self.console is not None:
            if result:
                self.console(f"{self.host} Successfully query the value of redis key (string).")
            else:
                self.console(f"{self.host} Failed to query the value of redis key (string).")
        return result

    def set_json(
            self,
            key: str,
            value: Dict[str, any],
            ex=EXPIRE_TIME
    ) -> bool:
        """
        Store redis hash type data (json).
        """
        try:
            # If value is a dict, serialize it.
            duplicate = copy.deepcopy(value)
            for k, v in value.items():
                duplicate.update({
                    k: json.dumps(v, cls=AdvancedEncoder, ensure_ascii=False)
                })
            map = duplicate
            del duplicate
            # Hash map storage.
            self.conn.hset(name=key, mapping=map)
            self.conn.save()
            # Define expiration time.
            self.conn.expire(name=key, time=ex)
            if self.console is not None:
                self.console(f"{self.host} Successfully set the value of redis key (json).")
            return True
        except:
            if self.console is not None:
                self.console(f"{self.host} Failed to set the value of redis key (json).")
            return False

    def get_json(self, key: str) -> Dict[str, any]:
        """
        View redis hash type data (json).
        """
        result = {}
        container = {}
        convert = None
        data = self.conn.hgetall(name=key)
        if data:
            for k, v in data.items():
                try:
                    # If there is a value in json format, try to deserialize it.
                    convert = json.loads(v.decode(self.CHAR_ENCODING))
                except:
                    # Use the default string type.
                    convert = v.decode(self.CHAR_ENCODING)
                finally:
                    container.update({
                        k.decode(self.CHAR_ENCODING): convert
                    })
        if container:
            result.update({
                key: container
            })
            if self.console is not None:
                self.console(f"{self.host} Successfully query the value of redis key (json).")
        else:
            if self.console is not None:
                self.console(f"{self.host} Failed to query the value of redis key (json).")
        return result

    @property
    def keys(self) -> List[str]:
        key_lists = self.conn.keys()
        result = [k.decode(self.CHAR_ENCODING) for k in key_lists]
        if self.console is not None:
            if result:
                self.console(f"{self.host} Successfully list the keys.")
            else:
                self.console(f"{self.host} Failed to list the keys.")
        return result

    def _quiet(self):
        if self.conn:
            self.conn.close()
        return None


