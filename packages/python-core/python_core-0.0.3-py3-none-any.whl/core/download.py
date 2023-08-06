
"""
    core/download.py

    useful for downloading
    stuff from internet

    author: @alexzander
"""


# python
import json
import requests

# 3rd party
from bs4 import BeautifulSoup # pip install bs4
from requests_html import HTMLSession # pip install requests_html

# core package ( pip install python-core )
from core.__json import *


def download_image_from_url(url, destination):
    """ returns the absolute path of the destination """
    if type(url) != str or type(url) != str:
        raise TypeError("incorrect type.")
    if not url.startswith("http://") and not url.startswith("https://"):
        raise ValueError("not valid url.")
    if "/" not in destination and "\\" not in destination:
        raise ValueError

    response = requests.get(url, stream=True)
    response.raw.decode_content = True

    # try:
    #     with open(destination, "xb+") as binaryfile:
    #         binaryfile.write(response.raw.data)
    # except FileExistsError:
    with open(destination, "wb") as binaryfile:
        binaryfile.write(response.raw.data)
    return destination


def download_file_from_url(url, folder, headers={}, name="", extension=""):
    response = requests.get(url, headers=headers, stream=True)
    response.raw.decode_content = True

    if name == "" and extension == "":
        items = url.split("/")
        filename = items[len(items) - 1]
        fullpath = folder + "\\" + filename
        del items, filename
    else:
        if folder.endswith("\\"):
            fullpath = folder + name + "." + extension
        else:
            fullpath = folder + "\\" + name + "." + extension

    with open(fullpath, "wb") as binaryfile:
        binaryfile.truncate(0)
        binaryfile.write(response.raw.data)
    return fullpath


def get_yt_video_thumbnail_url(url):
    if type(url) != str:
        raise TypeError

    if not url.startswith("https://www.youtube.com/watch?v="):
        raise ValueError

    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=1)

    soup = BeautifulSoup(response.html.html, "html.parser")
    webelement = soup.find("script", attrs={"class": "style-scope ytd-player-microformat-renderer"})

    data = json.loads(webelement.text)
    return data["thumbnailUrl"][0]