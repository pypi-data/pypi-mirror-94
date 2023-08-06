
"""
    core/exceptions.py

    useful custom exceptions for
    different cases

    author: @alexzander
"""


# core package ( pip install python-core )
from core.system import *
from core.aesthetics import *


class core_Exception(Exception):
    def __init__(self, message=""):
        self.message = message


class RuntimeError(core_Exception):
    """ error during execution """
    pass


class HTTP_RequestError(core_Exception):
    """ handles the http stuff"""
    pass


class NotFound_404_Error(HTTP_RequestError):
    """ 404 http error """
    pass


class Forbidden_403_Error(HTTP_RequestError):
    """ 403 http error """
    pass


class StupidCodeError(core_Exception):
    pass


class StopRecursive(core_Exception):
    pass


class NotFoundError(core_Exception):
    pass