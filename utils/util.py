# -*- coding: UTF-8 -*-
from typing import TypeVar, Union
from importlib import import_module
from config.settings import INSTALLED_ROUTES

T = TypeVar('T')       # Can be anything


def import_members(key: str) -> Union[T]:
    """
    [recommend]
    This way replaces the classic import module.
    """
    route = [i for i in INSTALLED_ROUTES if key == i.split(".")[-1]][0]
    func = lambda s: (".".join(s.split(".")[:-1]), s.split(".")[-1])
    a, b = func(route)
    module = import_module(a)
    # print(dir(module))
    obj = getattr(module, b)
    return obj


def dynamic_import() -> dict:
    """
    [unstable]
    See how unit_test.py is referenced.
    """
    # return (str(item.split('.')[-1]) for item in INSTALLED_ROUTES)
    for item in INSTALLED_ROUTES:
        func = str(item.split('.')[-1])
        exec(f"{func} = import_members('{func}')")
    local_dicts = locals()
    local_dicts.pop('item')
    local_dicts.pop('func')
    return local_dicts


