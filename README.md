# 更高效的数据库操作工具
Database connection pool packaging tool
---

## 概述说明
Python 语言数据库建连与 Logger 日志的模块简易封装。

## 实现功能
- 可连接 Redis，CURD，集成 set 与 hset 方式
- 可连接 MySQL，CURD

## 集成方法
- 将所有目录clone到本地，修改 config 中的文件
  - **config.prd.yml** 数据库连接选项
  - **settings.py** 模块装配定义
- 可在 service 中添加你的业务逻辑代码
- 可在 utils 包中添加通用的方法

## 功能细节
- 使用 PEP 585 的 Generics 注解风格
- 使用 enum 和 dataclass 的常量定义
- 类中 **kwargs 变长参数的自动初始化
- 仿 Django 的 settings 可插拔式设计
- Python 中对 Json 序列化格式的增强

## 部署使用
1. shell：自动检索与 function 的装配;
2. 自定义 yaml 文件;
3. 主入口文件为: manage.py

## 示例运行
```shell
# 编辑YAML配置文件
[root@localhost ./db-manager-service] # vim config/config.prd.yml

# Prd环境: 密码不建议直接写在YAML配置里
# Stage环境可随意, 
# 生产可随Pod启动写入系统环境变量,
# 程序会读取环境变量
[root@localhost ./db-manager-service] # echo "export REDIS_PASSWD=\"abcde@12345\"" >> ${HOME}/.bashrc

# 自动装配路由
[root@localhost ./db-manager-service] # bash tools/installed_routes.sh
function loaded successfully!

# 检查装配结果
[root@localhost ./db-manager-service] # sed -n '/INSTALLED_ROUTES/,/}/p' config/settings.py
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

# 编写业务逻辑
[root@localhost ./db-manager-service] # vim service/example.py

# 运行工具
[root@localhost ./db-manager-service] # python3 manage.py
2022-06-01 06:32:53 | redis_ops.py: 87 | redis_ops:set_string | [INFO] 10.0.0.88 Successfully set the value of redis key (string).
2022-06-01 06:32:53 | redis_ops.py:144 | redis_ops:set_json | [INFO] 10.0.0.88 Successfully set the value of redis key (json).
2022-06-01 06:32:53 | redis_ops.py:188 | redis_ops:  keys | [INFO] 10.0.0.88 Successfully list the keys.
2022-06-01 06:32:53 | redis_ops.py:115 | redis_ops:get_string | [INFO] 10.0.0.88 Successfully query the value of redis key (string).
2022-06-01 06:32:53 | redis_ops.py:176 | redis_ops:get_json | [INFO] 10.0.0.88 Successfully query the value of redis key (json).
2022-06-01 06:32:53 | redis_ops.py: 68 | redis_ops:del_keys | [INFO] 10.0.0.88 Successfully delete the redis keys.
---------------------------------------------------------------------------------------------------------------------------------------
command> keys *     : ['info', 'users']
command> get        : {'users': ['mystic', 'king', 'araon']}
command> hgetall    : {'info': {'data': {'name': 'mystic', 'age': 20, 'location': ['Beijing', 'Qingdao', 'Shanghai']}, 'level': 1}}
---------------------------------------------------------------------------------------------------------------------------------------
```
