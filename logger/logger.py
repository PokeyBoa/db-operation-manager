# -*- coding: UTF-8 -*-
import os
import sys
import logging
from utils.const import LogLevel


class Logger(object):

    """
    日志模块的封装, 日志级别分别是 debug/info/warning/error/critical
    支持保存到 /tmp/logs/xxx.log, 或者直接输出到 Console 终端上。
    """

    # 日志目录与文件相关
    __base_dir = "/tmp"
    __log_dir = os.path.join(__base_dir, "logs")
    __file_all = os.path.join(__log_dir, "project-all.log")
    __file_err = os.path.join(__log_dir, "project-error.log")

    # 日志级别关系映射
    __level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    # 定义日志输出格式
    __formatter = "%(asctime)s | %(filename)10s:%(lineno)3d | %(module)8s:%(funcName)6s | [%(levelname)s] %(message)s"

    def __init__(
        self,
        level: str = 'info',
        fmt: str = __formatter,
        when: str = 'D',
        backCount: int = 3,
        name: str = 'log'
    ):
        # 设置日志级别
        self.level = level

        # 记录到文件所需参数
        self.when = when
        self.backCount = backCount

        # 给日志对象设置个名字
        self.name = name

        # 设置日志格式
        self.format_str = logging.Formatter(
            fmt, datefmt="%Y-%m-%d %H:%M:%S")

        # 获取logger对象
        self.logger = logging.getLogger(self.name)

        # 设置日志级别
        self.logger.setLevel(self.__level_relations.get(self.level))


    def __mkdir(self) -> None:
        """
        创建日志目录
        """
        if os.path.exists(self.__base_dir) and os.path.isdir(self.__base_dir):
            if not os.path.exists(self.__log_dir) or not os.path.isdir(self.__log_dir):
                os.mkdir(self.__log_dir)
        else:
            os.mkdir(self.__base_dir)
            os.mkdir(self.__log_dir)

    @property
    def savelog(self) -> None:
        """
        interval是时间间隔，backupCount是备份文件的个数，如果超过这个个数，就会自动删除，when是间隔的时间单位，单位有以下几种：
        S 秒
        M 分
        H 小时
        D 天
        W 每星期（interval==0时代表星期一）
        midnight 每天凌晨
        """
        if self.level in ['debug', 'warning', 'error', 'critical']:
            _filename = self.__file_all
        elif self.level in ['info']:
            _filename = self.__file_err
        else:
            sys.exit("\nPlease enter an acceptable level value.")
        self.__mkdir()

        # 向文件中输出, 指定间隔时间自动生成文件的处理器
        # 实例化TimedRotatingFileHandler
        fileHandler = handlers.TimedRotatingFileHandler(
            filename=_filename,
            when=self.when,
            backupCount=self.backCount,
            encoding='utf-8'
        )
        # 设置文件里写入的格式
        fileHandler.setFormatter(self.format_str)
        # 把对象加到logger里
        self.logger.addHandler(fileHandler)
        return None

    def terminal(self) -> None:
        # 往屏幕上输出
        consoleHandler = logging.StreamHandler()
        # 设置屏幕上显示的格式
        consoleHandler.setFormatter(self.format_str)
        # 把对象加到logger里
        self.logger.addHandler(consoleHandler)
        return None


def Console(level: int = 2) -> object:
    """
    输出到console终端
    """
    grade = LogLevel().LOG_Level_List
    if 0 < level < len(grade) + 1:
        value = grade[level-1]
    else:
        sys.exit("\n选择以下的值: \ndebug : 1\ninfo  : 2\nwarn  : 3\nerr   : 4\ncrit  : 5")

    log = Logger(level=value)
    log.terminal()
    handler = eval(f"log.logger.{value}")
    return handler

