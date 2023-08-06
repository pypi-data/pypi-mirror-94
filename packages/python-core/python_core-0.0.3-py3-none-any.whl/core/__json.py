
"""
    core/__json.py

    upgraded version of json.py
    useful in work with jsons

    author: @alexzander
"""


# python
import os
import json

# core package ( pip install python-core )
from core.system import *
from core.__path import *


def json_dumps(__json: dict, __indent=4):
    return json.dumps(__json, indent=__indent)


def read_json_from_file(__path: str):
    """ reads .json from @path"""

    # validation
    if not is_file(__path):
        raise ValueError

    # read
    return json.loads(open(__path, "r+", encoding="utf-8").read())


def write_json_to_file(__json: dict, dst: str):
    """ writes dict or list from @dumped_json to @destination_path"""

    # validation
    # if not os.path.exists(destination_path):
    #     raise ValueError
    if type(__json) not in [dict, list]:
        raise TypeError

    # write
    with open(dst, "w+", encoding="utf-8") as _json:
        _json.truncate(0)
        _json.write(json.dumps(__json, indent=4))


def prettify(__collection, __indent=4):
    return json.dumps(__collection, indent=__indent)


def pretty_print(__collection, __indent=4):
    print(prettify(__collection, __indent=__indent))


# TESTING
if __name__ == '__main__':
    pass