# -*- coding: UTF-8 -*-
import os
import sys
from typing import Dict, List, Tuple, Union
from utils.util import import_members
from config.settings import SYS_ENV_PASSWORD

# import function members
FilePath = import_members("FilePath")
FileReader = import_members("FileReader")
DBConst = import_members("DBConst")
RedisOps = import_members("RedisOps")
LogLevel = import_members("LogLevel")


# Database operations
def auto_connect(component: str, log: str = 'info') -> object:
    # Check database selection.
    if component.lower() != DBConst.REDIS_COMPONENT:
        sys.exit('\nInvalid func parameter input.')

    # Check log level.
    log_list = LogLevel().LOG_Level_List
    if log.lower() not in log_list:
        _level = None
    else:
        _level = [int(i+1) for i, j in enumerate(log_list) if log.lower() == j][0]

    # get yaml filepath -> type: <enum 'FilePath'>
    yaml: Union[FilePath.CONF_YAML] = FilePath.CONF_YAML

    # Check whether the path is a real file.
    fp = FileReader(str(yaml))

    # Read and parse yaml file.
    content = fp.scan()[0]

    # Get log content from yaml file.
    log_args = [i for i in content['log']]
    for i in log_args:
        level = i.get('level')
        if level:
            break
    for i in log_args:
        status = str(i.get('status'))
        if status:
            break

    # Get level:
    # [priority] yaml config file > utils.const value
    try:
        if isinstance(level, int):
            if 0 >= level or level > len(log_list):
                sys.exit('\nInvalid yaml parameter input.')
        elif isinstance(level, str) and level.lower() in log_list:
            level = [int(i+1) for i, j in enumerate(log_list) if level.lower() == j][0]
        else:
            sys.exit('\nInvalid yaml parameter input.')
    except:
        pass
    finally:
        if not level:
            level = int(_level) if _level is not None else 2

    # Get status:
    # [priority] control yaml only
    # 'open' or 'close' | True or False | 1 or 0 | 'yes' or 'no'
    if status.lower() in ('open', 'true', '1', 'yes', 'none', 'y'):
        status = 1
    elif status.lower() in ("close", 'false', '0', 'no', 'n'):
        status = 0
    else:
        sys.exit('\nInvalid yaml parameter input.')
    # if status == 'close'; then close log print.
    if status == 0:
        level = None

    # Get db content from yaml file.
    db_args = lambda data: [i[component] for i in data['conn']
                            if component in i.keys()][0]
    getDB_args = db_args(content)

    # Get host:
    ipaddr = getDB_args.get("host")
    if ipaddr is None:
        sys.exit("\nhost not found.")

    # Get password:
    # [priority] yaml config file > os env variable
    password = getDB_args.get("passwd")
    if password is None:
        password = os.getenv(SYS_ENV_PASSWORD.get(DBConst.REDIS_COMPONENT))
        if password is None:
            sys.exit("\npasswd not found.")

    # Get port:
    # [priority] yaml config file > utils.const value
    port = getDB_args.get("port")
    if not port or not isinstance(port, int):
        port = DBConst.REDIS_LISTENING_PORT

    # Summarize database connection parameters.
    config = {
        'ipaddr': ipaddr,
        'password': password,
        'port': port,
        'component': component
    }

    # Use with context to connect to database.
    with RedisOps(level=level, **config) as handler:
        # Test response
        if handler.ping_pong:
            return handler
        return None


# Redis update data
def update(this=None, command=None, key=None, value=None) -> bool:
    if command.lower() == "set":
        this.set_string(key, value)
    elif command.lower() == "hset":
        this.set_json(key, value)
    else:
        return False
    return True


# Redis query data
def query(this=None, command=None, key=None) -> object:
    if command.lower() == "get":
        result = this.get_string(key=key)
    elif command.lower() == "hgetall":
        result = this.get_json(key=key)
    else:
        return None
    return result


# Redis delete data
def delete(this=None, keys=None) -> bool:
    if isinstance(keys, tuple):
        this.del_keys(keys)
        return True
    return False


# Redis list all keys
def select(this=None) -> List[str]:
    key_lists = this.keys
    return key_lists


# get connection handler
o = auto_connect(component='redis', log='warning')


# Redis curd operation
def Operator(
        client: object = o,
        command: str = None,
        key: Union[str, Tuple[str]] = None,
        value: Union[str, Dict[any, any]] = None
):
    result = None

    # curd method collection
    method = {
        "set": update,
        "hset": update,
        "get": query,
        "hgetall": query,
        "del": delete,
        "keys": select
    }

    # update data
    if command.lower() in ("set", "hset"):
        result = method.get(command)(
            this=client,
            command=command,
            key=key,
            value=value
        )
    # query data
    elif command.lower() in ("get", "hgetall"):
        result = method.get(command)(
            this=client,
            command=command,
            key=key
        )
    # delete data
    elif command.lower() == "del":
        result = method.get(command)(
            this=client,
            keys=key
        )
    elif command.lower() == "keys":
        result = method.get(command)(
            this=client
        )

    return result


