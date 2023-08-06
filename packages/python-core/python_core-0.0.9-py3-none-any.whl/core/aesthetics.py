
"""
    core/aesthetics.py

    useful and fancy design in terminal

    here you can
        - asciify text
        - color asciified text
        - color normal text

    author: @alexzander
"""


# python
import json
import requests

# core package ( pip install python-core )
from core.exceptions import *


impressive_fonts = [
    "bell",
    "big",
    "broadway",
    "bubble",
    "chunky",
    "contessa",
    "cursive",
    "cyberlarge",
    "cybermedun",
    "cybersmall",
    "digital",
    "doh",
    "doom",
    "double",
    "drpepper",
    "epic",
    "fender",
    "kban",
    "l4me",
    "larry3d",
    "ogre",
    "rectangles",
    "shadow",
    "slant",
    "small",
    "smkeyboard",
    "speed",
    "standard",
    "weird"
]


def asciify(text, font=None):
    """ puts 2 lines of spaces
         after the modified text. """
    if type(text) != str:
        text = str(text)
    if font not in impressive_fonts:
        raise NotFoundError

    text = "+".join(text.split())

    if font:
        url_parameters = f"/make?text={text}&font={font}"
    else:
        url_parameters = f"/make?text={text}"

    url = "http://artii.herokuapp.com"
    response = requests.get(url + url_parameters)
    if response.status_code != 200:
        raise ConnectionError("status code: {}".format(response.status_code))
    ascii_art = response.text
    items = ascii_art.split("\n")

    # deleting last 2 lines from the big text
    items = items[:len(items) - 2]
    # inserting "\n" because in original text it didnt exist
    items[len(items) - 1] += "\n"
    # reconstructing
    ascii_art = "\n".join(items)
    return ascii_art


def shift_left_ascii(ascii_text, size):
    """ left shift the big text with specified
        before:
        BIG_TEXT
        after:
        --------->(size) BIG_TEXT
    """
    if type(size) != int:
        raise TypeError

    if type(ascii_text) != str:
        raise TypeError

    if not "\n" in ascii_text:
        raise ValueError

    lines = ascii_text.split("\n")
    lines = [" " * size + line for line in lines]
    lines = "\n".join(lines)
    return lines


def shift_right_ascii(ascii_text, size):
    if type(size) != int:
        raise TypeError

    if type(ascii_text) != str:
        raise TypeError

    if not "\n" in ascii_text:
        raise ValueError

    lines = ascii_text.split("\n")
    lines = [line[size:] for line in lines]
    lines = "\n".join(lines)
    return lines


# text effects
endc_effect = "\033[0m"
bold_effect = "\033[1m"
underline_effect = "\033[4m"


ansi_codes = {
    'purple': '\033[95m',
    'blue': '\033[94m',
    'green': '\033[92m',
    'yellow': '\033[93m',
    'red': '\033[91m',
    'endc': '\033[0m',
    'bold': '\033[1m',
    'underlined': '\033[4m',
    'white': "\u001b[37;1m",
    "cyan": '\x1b[38;5;44m',
    "darkcyan": '\033[36m',
    "magenta": "\033[35m",
    "black": "\033[30m",
    "grey": "\x1b[38;5;246m",
    "orange": "\x1b[38;5;208m"
}


def ansi_colored(string, red, green, blue):
    if type(red) != int or \
       type(green) != int or \
       type(blue) != int or \
       type(string) != str:
        raise TypeError

    return "\x1b[{};{};{}m{}{}".format(red, green, blue, string, endc_effect)


def underline_effect(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError
    return ansi_codes["underlined"] + string + endc_effect


def bold_effect(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError
    return ansi_codes["bold"] + string + endc_effect


def ConsoleColored(string, color, bold=0, underlined=0):
    if type(string) != str:
        try:
            string = str(string)
        except Exception as error:
            print(error)
            message = red + ansi_codes["bold"] + 'type of param @string should be str.' + endc_effect
            raise TypeError(message)
            del message

    # incorrect color
    if color not in ansi_codes and color != 'random':
        message = red + ansi_codes["bold"] + 'this color "{}" is not in ANSICodesDICT.'.format(color) + endc_effect
        raise NotImplementedError(message)
        del message

    # bold == 0 and underlined == 0
    if not bold and not underlined:
        if color == "random":
            from random import choice
            return ansi_codes[choice(list(ansi_codes.keys()))] + string + endc_effect

        return ansi_codes[color] + string + endc_effect

    # bold == 0 and underlined == 1
    elif not bold and underlined:
        if color == "random":
            from random import choice
            return ansi_codes[choice(list(ansi_codes.keys()))] + \
                ansi_codes["underlined"] + string + endc_effect

        return ansi_codes[color] + ansi_codes["underlined"] + string + endc_effect

    # bold == 1 and underlined == 0
    elif bold and not underlined:
        if color == "random":
            from random import choice
            return ansi_codes[choice(list(ansi_codes.keys()))] + \
                ansi_codes["bold"] + string + endc_effect

        return ansi_codes[color] + ansi_codes["bold"] + string + endc_effect

    # bold == 1 and underlined == 1
    if color == "random":
        from random import choice
        return ansi_codes[choice(list(ansi_codes.keys()))] + \
            ansi_codes["bold"] + ansi_codes["underlined"] + string + endc_effect

    return ansi_codes[color] + ansi_codes["bold"] + ansi_codes["underlined"] + string + endc_effect


def print_ansi_table():
    import sys
    print("\n")
    for i in range(0, 16):
        for j in range(0, 16):
            code = str(i * 16 + j)
            sys.stdout.write(u"\u001b[38;5;" + code + "m " + code.ljust(4))
        print (u"\u001b[0m")
    print("\n")


import re

ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")

def delete_ansi_escape_codes(string):
    if type(string) != str:
        try:
            string = str(string)
        except:
            raise TypeError

    return ansi_escape.sub("", string)


# ---------------------------------------------------------
# printing colored

def print_red(__string):
    print(ConsoleColored(__string, "red"))


def print_blue(__string):
    print(ConsoleColored(__string, "blue"))


def print_yellow(__string):
    print(ConsoleColored(__string, "yellow"))


def print_orange(__string):
    print(ConsoleColored(__string, "orange"))


def print_purple(__string):
    print(ConsoleColored(__string, "purple"))


def print_cyan(__string):
    print(ConsoleColored(__string, "cyan"))


def print_green(__string):
    print(ConsoleColored(__string, "green"))


# ---------------------------------------------------------
# printing colored UNDERLINED

def print_red_underlined(__string):
    print(ConsoleColored(__string, "red", underlined=1))


def print_blue_underlined(__string):
    print(ConsoleColored(__string, "blue", underlined=1))


def print_yellow_underlined(__string):
    print(ConsoleColored(__string, "yellow", underlined=1))


def print_orange_underlined(__string):
    print(ConsoleColored(__string, "orange", underlined=1))


def print_purple_underlined(__string):
    print(ConsoleColored(__string, "purple", underlined=1))


def print_cyan_underlined(__string):
    print(ConsoleColored(__string, "cyan", underlined=1))


def print_green_underlined(__string):
    print(ConsoleColored(__string, "green", underlined=1))


# ---------------------------------------------------------
# printing colored BOLD

def print_red_bold(__string):
    print(ConsoleColored(__string, "red", bold=1))


def print_blue_bold(__string):
    print(ConsoleColored(__string, "blue", bold=1))


def print_yellow_bold(__string):
    print(ConsoleColored(__string, "yellow", bold=1))


def print_orange_bold(__string):
    print(ConsoleColored(__string, "orange", bold=1))


def print_purple_bold(__string):
    print(ConsoleColored(__string, "purple", bold=1))


def print_cyan_bold(__string):
    print(ConsoleColored(__string, "cyan", bold=1))


def print_green_bold(__string):
    print(ConsoleColored(__string, "green", bold=1))


# ---------------------------------------------------------
# printing colored  BOLD + UNDERLINED

def print_red_bold_underlined(__string):
    print(ConsoleColored(__string, "red", bold=1, underlined=1))


def print_blue_bold_underlined(__string):
    print(ConsoleColored(__string, "blue", bold=1, underlined=1))


def print_yellow_bold_underlined(__string):
    print(ConsoleColored(__string, "yellow", bold=1, underlined=1))


def print_orange_bold_underlined(__string):
    print(ConsoleColored(__string, "orange", bold=1, underlined=1))


def print_purple_bold_underlined(__string):
    print(ConsoleColored(__string, "purple", bold=1, underlined=1))


def print_cyan_bold_underlined(__string):
    print(ConsoleColored(__string, "cyan", bold=1, underlined=1))


def print_green_bold_underlined(__string):
    print(ConsoleColored(__string, "green", bold=1, underlined=1))


# ---------------------------------------------------------
# returning colored

def yellow(__string):
    return ConsoleColored(__string, "yellow")


def orange(__string):
    return ConsoleColored(__string, "orange")


def purple(__string):
    return ConsoleColored(__string, "purple")


def cyan(__string):
    return ConsoleColored(__string, "cyan")


def green(__string):
    return ConsoleColored(__string, "green")


def red(__string):
    return ConsoleColored(__string, "red")


def blue(__string):
    return ConsoleColored(__string, "blue")


# ---------------------------------------------------------
# returning colored UNDERLINED

def yellow_underlined(__string):
    return ConsoleColored(__string, "yellow", underlined=1)


def orange_underlined(__string):
    return ConsoleColored(__string, "orange", underlined=1)


def purple_underlined(__string):
    return ConsoleColored(__string, "purple", underlined=1)


def cyan_underlined(__string):
    return ConsoleColored(__string, "cyan", underlined=1)


def green_underlined(__string):
    return ConsoleColored(__string, "green", underlined=1)


def red_underlined(__string):
    return ConsoleColored(__string, "red", underlined=1)


def blue_underlined(__string):
    return ConsoleColored(__string, "blue", underlined=1)


# ---------------------------------------------------------
# returning colored BOLD

def yellow_bold(__string):
    return ConsoleColored(__string, "yellow", bold=1)


def orange_bold(__string):
    return ConsoleColored(__string, "orange", bold=1)


def purple_bold(__string):
    return ConsoleColored(__string, "purple", bold=1)


def cyan_bold(__string):
    return ConsoleColored(__string, "cyan", bold=1)


def green_bold(__string):
    return ConsoleColored(__string, "green", bold=1)


def red_bold(__string):
    return ConsoleColored(__string, "red", bold=1)


def blue_bold(__string):
    return ConsoleColored(__string, "blue", bold=1)


# ---------------------------------------------------------
# returning colored BOLD + UNDERLINED

def yellow_bold_underlined(__string):
    return ConsoleColored(__string, "yellow", bold=1, underlined=1)


def orange_bold_underlined(__string):
    return ConsoleColored(__string, "orange", bold=1, underlined=1)


def purple_bold_underlined(__string):
    return ConsoleColored(__string, "purple", bold=1, underlined=1)


def cyan_bold_underlined(__string):
    return ConsoleColored(__string, "cyan", bold=1, underlined=1)


def green_bold_underlined(__string):
    return ConsoleColored(__string, "green", bold=1, underlined=1)


def red_bold_underlined(__string):
    return ConsoleColored(__string, "red", bold=1, underlined=1)


def blue_bold_underlined(__string):
    return ConsoleColored(__string, "blue", bold=1, underlined=1)


# TESTING
if __name__ == '__main__':
    print(asciify("hello"))