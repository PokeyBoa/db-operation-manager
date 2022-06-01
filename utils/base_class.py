# -*- coding: UTF-8 -*-
import inspect

class KwargsClass(object):

    """
    Use 'self.attributes' to observe the
    corresponding variable-length arguments.
    """

    def __init__(self, **kwargs):
        # Collect keys for all properties
        self.attributes = dict()

        # Get positional params dynamically
        argspec = inspect.getfullargspec(self.__class__)

        # Get **kwargs dynamically
        if argspec.varkw:
            param_keys = []
            for k, v in kwargs.items():
                param_keys.append(k)
                self.__setattr__(k, v)
            self.attributes.update({'kwargs': param_keys})

        # View the self member variable
        # self.__repr__()

    def __repr__(self):
        """Debugging: Viewing Class Object Properties"""
        print(self.__dict__)
        return super(self.__class__, self).__repr__()

    @property
    def _keys(self):
        for i in self.attributes.values():
            kwargs = ", ".join(i)
        width = len(kwargs)
        width += 10 - width % 10
        line = "─" * width * 2
        report = "\n" + line + f"\n{'NAME':^{width}}│{'KEYS':^{width-1}}\n" + \
        line + f"\n{'this':<{width}}│{'self':>{width-1}}" + \
        f"\n{'**kwargs':<{width}}│{kwargs:>{width-1}}\n" + line + "\n"
        return report


