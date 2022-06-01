# -*- coding: UTF-8 -*-
import os
import sys
import yaml
import json
import codecs
import inspect
import warnings
import configparser
from itertools import islice
from typing import (
    Dict,
    List,
    NoReturn,
    Optional
)
from utils.const import FileType as ft
from utils.const import FileFormat as ff


def file_exist(filename: str) -> (bool, str):
    """
    A function that determines the authenticity of a file and returns its file type.
    """
    if not os.path.exists(filename):
        flag, type = False, ft.NULL
    else:
        if os.path.isfile(filename):
            flag, type = True, ft.FILE
        elif os.path.isdir(filename):
            flag, type = True, ft.DIR
        elif os.path.islink(filename):
            flag, type = True, ft.LINK
        else:
            flag, type = True, ft.OTHER
    return flag, type


def file_format(filename: str) -> str:
    """
    A function that returns the file types it supports in a qualified enumeration.
    Returns a string like 'py', 'sh', etc. if supported, otherwise returns an empty string.
    """
    suffix = os.path.splitext(filename)[-1][1:]
    extension = lambda f: [i.value for i in list(ff) if f == i][0] \
        if [i for i in ff if f == i] else ""
    return extension(suffix)


class FileReader(object):

    """
    Abstract base class for implementing the automatic content
    parsing of specified file types.
    """

    def __init__(self, filename: str) -> None or NoReturn:
        self.action = None
        self.filename = filename
        self.data, self.container = [], []
        if not self.file_filter:
            sys.exit(f'Please check if the absolute path of '
                     f'the file exists.\n{self.filename}')

    @property
    def file_filter(self) -> bool:
        """
        This function provides filtering of file authenticity
        and analyzes its extension.
        """
        _, ftype = file_exist(self.filename)
        if ftype == ft.FILE:
            self.this_suffix = file_format(self.filename)
            if self.this_suffix:
                return True
        return False

    def parse_yaml(self) -> List[str]:
        """
        Parse the yaml into a list of dict elements.
        """
        if self.this_suffix == ff.FILE_YAML:
            with open(self.filename) as f:
                self.data = yaml.load(f, Loader=yaml.FullLoader)
        return self.data

    def parse_text(self) -> List[str]:
        """
        Parse the text, removing \n characters from each line.
        """
        with open(file=self.filename, mode='rt', encoding='utf-8') as f:
            for line in f:
                self.data.append(line.strip())
        return self.data

    def parse_json(self) -> Dict[str, any]:
        """
        Parse the json, read data and deserialize to Python data type.
        """
        with open(file=self.filename, mode='rt', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data

    def parse_ini(self) -> List[Dict[str, any]]:
        """
        Parse the ini, Generally used for configuration files.
        """
        config = configparser.ConfigParser()
        config.read(filenames=self.filename, encoding='utf-8')
        section_list = config.sections()
        for title in section_list:
            item_list = config.items(title)
            group = {title: item_list}
            self.data.append(group)
        return self.data

    def parse_csv(self, skiphead: bool = False) -> List[List[str]]:
        """
        Parse the csv, removing \n characters from each line,
        split each field, and option to ignore header row.
        """
        warnings.warn(
            "To filter the header of the first line of the csv file,"
            "Use 'FileReader.parse_csv()' instead.",
            FutureWarning, stacklevel=5
        )
        # Skip the first line with idx=0 and
        # start reading the file from idx=1.
        start = 1 if skiphead else 0
        count = 0
        with codecs.open(
                filename=self.filename,
                mode='rb',
                encoding='utf-8',
                errors='strict',
                buffering=-1
        ) as f:
            for _, line in enumerate(islice(f, start, None)):
                line_list = line.strip().split(',')
                self.data.append(line_list)
                count += 1
        return self.data

    def __method_mapping(self) -> None:
        """
        This function provides a list container for storing method maps.
        """
        for i, j in inspect.getmembers(ff):
            if i.startswith("FILE"):
                func_name = f"parse_{j.replace('yml', 'yaml').replace('txt', 'text')}"
                for k, v in inspect.getmembers(self):
                    if k.startswith("parse"):
                        if func_name == k:
                            element = {
                                "func_call": v,
                                "enum_attr": i,
                                "file_suffix": j.value
                            }
                            self.container.append(element)

    def scan(self) -> Optional[List[str] or Dict[str, any] or None]:
        """
        This function automatically adapts the file format for preview,
        which is implemented by reflection and __call__ magic method.
        """
        self.__method_mapping()
        for item in self.container:
            if item.get('file_suffix') == self.this_suffix:
                format_lists = ff._member_names_
                for attr in format_lists:
                    if self.this_suffix == getattr(ff, attr):
                        self.action = item.get('func_call')
        if self.action and callable(self.action):
            # self.action.__repr__()
            content = self.action.__call__()
            return content
        return None

    #------------------------------------------------------------------------------
    # Fatal: maximum recursion depth exceeded while calling a Python object.
    # def setfunc(self, val):
    #     self.placeholder = val
    # def delfunc(self):
    #     self.placeholder = None
    # preview = property(reader, setfunc, delfunc, "")
    #------------------------------------------------------------------------------


