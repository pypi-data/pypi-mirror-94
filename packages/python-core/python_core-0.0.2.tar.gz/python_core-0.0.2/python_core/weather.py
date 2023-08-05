
"""
    system.py

    wheather module wrapped around
    pyowm ( open wheather map api)

    author: @alexzander
"""


# 3rd party
from pyowm import OWM

# core package (pip install python-core)
from core.system import *


class Wheather(OWM):
    def __init__(self, api_key):
        self.api_key = api_key
        super().__init__(self.api_key)
        self.manager = self.weather_manager()


    def get_temperature(self, location, unit_measurement="celsius"):
        w = self.manager.weather_at_place(location).weather
        return w.temperature(unit_measurement)["temp"]



# TESTING
if __name__ == '__main__':
    # usage
    api_key = "your api key from open weather map website"
    w = Wheather(api_key)
    t = w.get_temperature("Aalbord")
    print(t)