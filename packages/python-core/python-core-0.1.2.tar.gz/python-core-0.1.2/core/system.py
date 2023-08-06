
"""
    system.py

    useful module in accesing and using system stuff

    author: @alexzander
"""


# python
import os
import sys
import platform
from time import sleep, time

# core package ( pip install python-core )
from core.aesthetics import *
from core.exceptions import *
from core.__numbers import *

# 3rd party
import cv2 # pip install opencv-python
import pyzbar # pip install pyzbar
import colored_traceback # pip install colored_traceback


def get_os():
    return platform.system()


def get_python_path():
    """ return folder path """
    if os.environ["PYTHONPATH"].endswith(";"):
        return os.environ["PYTHONPATH"][:-1]
    return os.environ["PYTHONPATH"]


def get_tesseract_path():
    """ return executable of tesseract engine (if installed) """
    if "TESS" not in os.environ.keys():
        raise NotFoundError("TESS is not environment variables")
    return os.environ["TESS"]


def colorize_error():
    colored_traceback.add_hook(always=True)


def clear_screen():
    """ clears the shell screen depending on the opearting system """
    o = get_os()
    if o == "Windows":
        os.system("cls")
    elif o == "Linux" or o == "Darwin":
        os.system("clear")


def pause_program(message="[ press {} to continue ... ]".format(green_bold("<enter>"))):
    input(message)


def get_device_name():
    return platform.node()


def get_arhitecture():
    return platform.architecture()[0]


def get_python_version():
    return platform.python_version()


def get_python_implementation():
    return platform.python_implementation()


def get_processor():
    return platform.processor()


def get_python_interpreter_path():
    return sys.executable


# TESTING
if __name__ == '__main__':
    o = get_os()
    print(o)