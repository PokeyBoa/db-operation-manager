# -*- coding: UTF-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(os.path.dirname(__file__))))
from config.settings import BASE_PATH
from utils.util import *
locals().update(dynamic_import())


# 引包的多种方式
def _unit_import_module():
    """
    随着引包的个数增加, 第三种动态导入方式越发明显
    方式三 > 方式二 > 方式一
    """
    # # 方式一
    # from logger.logger import Console

    # # 方式二
    # from utils.util import import_members
    # Console = import_members("Console")

    # # 方式三
    # from config.settings import INSTALLED_ROUTES
    # from utils.util import import_members
    # for item in INSTALLED_ROUTES:
    #     func = str(item.split('.')[-1])
    #     exec(f"{func} = import_members('{func}')")

    # # 方式四
    # for name in dynamic_import():
    #     exec(f"{name} = import_members('{name}')")
    pass


# 打印日志
def _unit_logger():
    console = Console(2)
    console("打印到终端")


# 打印路径
def _unit_filepath():
    res = FilePath.CONF_YAML
    print(res)


# 读取文件
def _unit_filereader():
    file = os.path.join(BASE_PATH, "config/config.prd.yml")
    fp = FileReader(file)
    content = fp.scan()[0]
    for k, v in content.items():
        print(k, v)


# 动态类参数信息
def _unit_argscls():
    # print(KwargsClass.__doc__)
    kwargs = {
        "ipaddr": "127.0.0.1",
        "port": 22,
        "password": "abcde@123",
        "node": "master"
    }
    obj = KwargsClass(**kwargs)
    # Use the 'keys' method to get a list of vals.
    print(obj.keys)
    # Get test object properties
    arglist = obj.attributes.get('kwargs')
    for i in arglist:
        if i.lower() in ["ipaddr", "host"]:
            print(eval(f"obj.{i}"))


# redis操作（低级封装）
def _unit_redisops():
    password = os.environ.get('REDIS_PASSWD')
    params = {
        'ipaddr': '10.0.0.88',
        'password': password,
        'component': 'redis',

    }
    with RedisOps(level=None, **params) as client:
        # 查询连接响应是否正常
        print(client.ping_pong)

        # 存储string(k-v)
        demo_list = ['mystic', 'king', 'araon']
        set_string = {
            "key": "users",
            "value": str(demo_list),
            "ex": 2 * 60
        }
        client.set_string(**set_string)

        # 存储hash(k-json)
        demo_json = {
            "姓名": "Mysitc",
            "学生": True,
            "心情": "😄",
            "年龄": 18,
            "学校": ['小学', '初中', '高中', '大学'],
            "爱好": {
                '游泳': {'自由泳', '潜水'},
                '滑雪': ['🏂', '🎿'],
                '游戏': ('LOL', 'PUBG', 'Genshin')
            }
        }
        set_json = {
            "key": "person",
            "value": demo_json,
            "ex": 3 * 60
        }
        client.set_json(**set_json)

        # 查询keys：返回存活的keys列表
        print(client.keys)

        # 查询string：输入key->返回value
        string = client.get_string(key="users")
        print(string)

        # 查询hash：输入key->返回value
        hash = client.get_json(key="person")
        print(hash)

        # 删除数据：可接收单个或多个（元组）
        client.del_keys(keys=("users", "person"))


# redis操作（高级封装: 建连/日志从yaml配置中获取，仅关注curd本身）
def _unit_rediscurd():
    # set命令：插入key-value(string)
    set_string = {
        "command": "set",
        "key": "users",
        "value": "['mystic', 'king', 'araon']"
    }
    Operator(**set_string)

    # hset命令：插入key-value(json)
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

    # keys命令：查看所有keys
    print(Operator(command="keys"))

    # get命令：查看value(string)
    get_string = {
        "command": "get",
        "key": "users"
    }
    print(Operator(**get_string))

    # hgetall命令：查看value(json)
    get_json = {
        "command": "hgetall",
        "key": "info"
    }
    print(Operator(**get_json))

    # del命令：删除单个或多个key(s) 元组类型
    del_keys = {
        "command": "del",
        "key": ("users", "info")
    }
    Operator(**del_keys)


if __name__ == '__main__':
    # _unit_filereader()
    # _unit_redisops()
    _unit_rediscurd()
    # _unit_logger()
    # _unit_argscls()
    # _unit_filepath()


