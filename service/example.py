# -*- coding: UTF-8 -*-
from utils.util import *
globals().update(dynamic_import())


def redis_curd_demo():
    # insert string type (str data)
    set_string = {
        "command": "set",
        "key": "users",
        "value": "['mystic', 'king', 'araon']"
    }
    Operator(**set_string)

    # insert hash type (json data)
    set_json = {
        "command": "hset",
        "key": "info",
        "value": {
            'level': 1,
            'data': {
                'name': 'mystic',
                'age': 20,
                'location': {'Beijing', 'Qingdao', 'Shanghai'}
            }
        }
    }
    Operator(**set_json)

    # view all keys
    all_keys = Operator(command="keys")

    # view value (string)
    get_string = {
        "command": "get",
        "key": "users"
    }
    data_str = Operator(**get_string)

    # view value (json)
    get_json = {
        "command": "hgetall",
        "key": "info"
    }
    data_dict = Operator(**get_json)

    # remove single or multiple key(s) tuple types
    del_keys = {
        "command": "del",
        "key": ("users", "info")
    }
    Operator(**del_keys)

    print("---" * 45)
    print("command> keys *     : {}".format(all_keys))
    print("command> get        : {}".format(data_str))
    print("command> hgetall    : {}".format(data_dict))
    print("---" * 45)


