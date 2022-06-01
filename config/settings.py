# -*- coding: UTF-8 -*-
import os

# Project root path.
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# You can customize the value, but please don't
# change the key, such as 'mysql', 'redis' etc.
# This option defines getting the corresponding
# password from `os.getenv('xxx')`. The Linux
# bash command is `export xxx="password"`.
SYS_ENV_PASSWORD = {
    'mysql': 'MYSQL_PASSWD',
    'redis': 'REDIS_PASSWD',
    'postgre': 'PGSQL_PASSWD'
}


# Defines the loading of functional functions.
INSTALLED_ROUTES = {
    "database.redis_curd.Operator",
    "database.redis_ops.RedisOps",
    "logger.logger.Logger",
    "logger.logger.Console",
    "utils.base_class.KwargsClass",
    "utils.const.DBConst",
    "utils.const.LogLevel",
    "utils.const.FilePath",
    "utils.file_util.FileReader",
    "utils.json_util.AdvancedEncoder",
}


# Other.


