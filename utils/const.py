# -*- coding: UTF-8 -*-
import os
from typing import List
from enum import Enum, unique
from dataclasses import dataclass, field
from config.settings import BASE_PATH


# Define database related constants
@dataclass(init=True, repr=True, eq=False, order=False, frozen=True)
class DBConst:
    """
    Use the dataclass decorator to initialize constants.
    """
    # dataclasses.field accepts a default_factory argument which can be
    # used to initialize the field if a value is not passed at the time
    # of creation of the object.
    _limit_tech = lambda: ["redis", "mysql", "postgre"]
    DB_COMPONENT_LIMIT: List[str] = field(default_factory=_limit_tech)

    # Unicode
    CHARACTER_ENCODING: str = "UTF-8"

    # Redis cache database
    REDIS_COMPONENT: str = "redis"
    REDIS_EXPIRE_TIME: int = 3 * 60 * 60
    REDIS_LISTENING_PORT: int = 6379
    REDIS_MAX_CONNS_LIMIT: int = 50

    # Mysql database
    MYSQL_COMPONENT: str = "mysql"
    MYSQL_LISTENING_PORT: int = 3306

    # Postgre database
    PGSQL_COMPONENT: str = "postgre"
    PGSQL_LISTENING_PORT: int = 5432


# Determine the level of the log
@dataclass(init=True, repr=True, eq=False, order=False, frozen=False)
class LogLevel:
    # output level list
    _grades = lambda: ['debug', 'info', 'warning', 'error', 'critical']
    LOG_Level_List: List[str] = field(default_factory=_grades)
    # def __post_init__(self):
    #     self.LOG_Level_List = self._grades()

    # output default level
    LOG_DEFAULT_LEVEL: str = "info"


# Define constants of enum.Enum types.
@unique
class FilePath(str, Enum):
    """
    A class that defines the enumeration values for this project path.
    """
    CONF_YAML = "config/config.prd.yml"

    def __init__(self, _):
        # 优化处理路径首尾拼接时, join 函数可能对 '/' 产生非预期结果
        filepath = lambda f: f[1:] if f.startswith(os.sep) else f
        self.abspath = os.path.join(BASE_PATH, filepath(self.value))

    def __str__(self):
        return self.abspath

@unique
class FileType(str, Enum):
    """
    A class that defines enumeration values for common file types.
    """
    NULL = "null"
    FILE = "file"
    DIR = "folder"
    LINK = "link"
    OTHER = "undefined"

    def __str__(self):
        return self.value

@unique
class FileFormat(str, Enum):
    """
    A class that defines enumeration values for common file suffix extensions.
    """
    # UNKNOWN = ""
    FILE_CSV = "csv"
    FILE_INI = "ini"
    FILE_YAML = "yml"
    FILE_JSON = "json"
    FILE_TEXT = "txt"
    FILE_SHELL = "sh"
    FILE_PYTHON = "py"

    def __str__(self):
       return self.value

    def __iter__(self):
        iter_obj = (i for i in FileFormat.__dict__.get('_member_names_'))
        return iter_obj


