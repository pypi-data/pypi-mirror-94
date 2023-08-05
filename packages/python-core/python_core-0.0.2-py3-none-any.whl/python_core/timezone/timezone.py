
"""

"""

# python
import os
from datetime import datetime

# 3rd party
import pytz # pip install pytz

# core package ( pip install python-core )
from core.__json import *
from core.__path import *


class timezone_Exception(Exception):
    def __init__(self, message=""):
        self.message = message


class TimezoneNotFoundError(timezone_Exception):
    pass


def get_current_timezone(location="Europe/Bucharest", time_format="%H:%M:%S"):
    """ @location: Continent/City"""
    if location not in pytz.all_timezones:
        raise TimezoneNotFoundError
    return datetime.now(pytz.timezone(location)).strftime(time_format)