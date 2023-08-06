
"""
    core/__datetime.py

    powerful time, date and datetime module
    useful in development of programs that
    work with the concept of time

    upgraded version of time.py and datetime.py

    author: @alexzader
"""


# python
import time
import calendar
from datetime import datetime

# core package ( pip install python-core )
from core.__numbers import *
from core.aesthetics import *


date_format = "%d.%m.%Y"
time_format = "%H:%M:%S"

datetime_format = "[ {} ] - [ {} ]".format(date_format, time_format)
timedate_format = "[ {} ] - [ {} ]".format(time_format, date_format)


def is_valid_date(date_str: str):
    try:
        datetime.strptime(date_str, date_format)
        return True
    except:
        return False


def is_valid_time(time_str: str):
    try:
        datetime.strptime(time_str, time_format)
        return True
    except:
        return False


def is_valid_datetime(datetime_str: str):
    try:
        datetime.strptime(datetime_str, datetime_format)
        return True
    except:
        return False


def get_current_date(__format=date_format):
    return datetime.now().strftime(__format)


def get_current_time(__format=time_format):
    return datetime.now().strftime(__format)


def get_current_datetime(__format=datetime_format):
    return datetime.now().strftime(__format)


def get_current_timedate(__format=timedate_format):
    return datetime.now().strftime(__format)


def get_execution_time(__function, *params):
    before = time()
    result = __function(*params)
    if result != None:
        print(result)

    duration = time() - before
    duration = fixed_set_precision_str(duration, 2)
    return duration


def print_execution_time(__function, *params):
    print("execution time: [ {} second(s) ]".format(yellow_bold(get_execution_time(__function, *params))))