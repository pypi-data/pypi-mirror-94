#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys
import json
import yaml
from xml.dom import minidom
import logging
from pprint import pformat

log = logging.getLogger(__name__)


def set_logger(lvl, log_file="/tmp/i2b2l.log"):
    sys.tracebacklimit = None if lvl == "DEBUG" else 0
    numlvl = 10 if lvl == "DEBUG" else 40
    handlers = [logging.StreamHandler(sys.stdout)]
    if log_file and os.path.isdir(log_file):
        handlers += [logging.FileHandler(log_file)]
    logging.basicConfig(
        handlers=handlers,
        level=numlvl,
        format="%(asctime)s | %(levelname)s | %(funcName)s: | %(message)s",
        datefmt="%H:%M:%S",
    )
    log.debug(f"Log level: {lvl}")
    log.debug(f"Traceback: {sys.tracebacklimit}")
    return log


def joinsep(lst, sep=", ", caps="__repr__"):
    return sep.join([getattr(x, caps)() for x in lst])


def safe_dump_json(data):
    return json.dumps(data, default=lambda o: f"{type(data).__qualname__}: {str(data)}")


def is_iterable(obj):
    try:
        iter(obj)
        return True
    except:
        return False


def filter_dict(data: dict, excl: list = None, incl: list = None) -> dict:
    """Filter given keys+values from dict either in- or exclusive.
    Args:
        data (dict): Dictionary to filter
        excl (list): If set, the keys in the list are excluded
        incl (list): If set, only the keys in the list are included
    """
    data = data if isinstance(data, dict) else data.__dict__
    new_data = {}
    for k, v in data.items():
        if excl and k in excl or k.startswith("_"):
            continue
        if incl and k not in incl:
            continue
        new_data[k] = v
    return new_data


def singleton(cls):
    """class decorator to implement singleton pattern
    @singleton
    class A: pass
    a1 = A()
    a2 = A.instance()
    assert a1 is a2
    """
    class SingleCls(cls):
        """ inner wrapper class """
        _inst = None
        inited = False

        def __new__(cls, *args, **kwargs):
            if cls._inst is None:
                cls._inst = object.__new__(cls)
            return cls._inst

        def __init__(self, *args, **kwargs):
            if not self.inited:
                self.inited = True
                super(SingleCls, self).__init__(*args, **kwargs)

        @classmethod
        def instance(cls):
            """ get the singleton instance """
            return cls._inst if cls._inst else cls()

    # simulate the name of input class
    SingleCls.__name__ = cls.__name__
    if hasattr(cls, "__qualname__"):  # python 2
        SingleCls.__qualname__ = cls.__qualname__
    SingleCls.__module__ = cls.__module__
    SingleCls.__doc__ = cls.__doc__
    return SingleCls


def format_return(func):
    """Format output of the decorated method

    This decorator looks for the keyword "fmt" in the decorated method
    and returns the formatted output.
    Options are:
    * str: Simply dump the data to its str() representation
    * yaml: Dump data to yaml.
            Be careful, yaml will serialize the whole data tree,
            often resulting in a mess
    * json: Dump data to json.
            Data may be truncated as json only dumps basic data structures
            (dict, list)
    * pretty: Return pformat(data). Trys to pretty-print python objects
    """
    # @functools.wraps(func)# Preserves function attributes, e.g. __doc__
    def format_return_wrapper(self="None", *args, **kwargs):
        cls = self.__class__.__name__ if isinstance(self, object) else __name__
        log.debug(f"{func.__name__}, {cls}, {args}, {kwargs}")
        data = func(self, *args, **kwargs)  # Store method output in data
        fmt = kwargs.get("fmt", None)  # Find "fmt" kwarg in kwargs
        if fmt is None:
            return data
        try:
            if fmt == "pretty":
                data = pformat(data)
            if fmt == "str":
                data = str(data)
            if fmt in ["yaml", "yml"]:
                data = yaml.dump(data)
            if fmt == "jsonl":
                if is_iterable(data):
                    data = [safe_dump_json(i) for i in data]
                else:
                    data = safe_dump_json(data)
            if fmt == "json":
                data = safe_dump_json(data)
            # If data is an XML Document or Element Object
            if isinstance(data, (minidom.Element, minidom.Document)):
                # Return prettified XML representation
                data = data.toprettyxml(indent="  ").replace("\n\n", "")
            if isinstance(data, (dict,)):
                data = str(data)
        except Exception as e:  # If something goes wrong:
            log.debug(f"{fmt}: {data}")  # Log format, data and error
            log.error(repr(e))
            data = str(data)
        return data  # Return data, formatted or not
    # Preserve function docstring
    format_return_wrapper.__doc__ = func.__doc__
    return format_return_wrapper


class SQLException(Exception):
    pass
