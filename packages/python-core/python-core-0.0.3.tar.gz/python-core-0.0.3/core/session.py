
"""
    core/session.py

    wrapped around bs4

    author: @alexzander
"""


# 3rd party
from bs4 import BeautifulSoup # pip install bs4
from requests_html import HTMLSession # pip install requrests_html

# core package ( pip install python-core )
from core.aesthetics import ConsoleColored


def get_soup(url, __print=False):
    fancy_url = ConsoleColored(url, "yellow", bold=1, underlined=1)
    if __print:
        print("HTTP GET request to URL: {} ...".format(fancy_url))

    session = HTMLSession()
    response = session.get(url)
    response.html.render(sleep=0.0001)
    if __print:
        print("creating soup...")
    soup = BeautifulSoup(response.html.html, "html.parser")
    if __print:
        print(ConsoleColored("soup created successfully.", "yellow", bold=1))
    return soup