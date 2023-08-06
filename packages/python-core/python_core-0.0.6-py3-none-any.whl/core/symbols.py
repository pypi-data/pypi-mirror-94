
"""
    core/symbols.py

    static symbols that can be
    imported to improve de design
    of a program

    author: @alexzander
"""


# core package (pip install python-core)
from core.aesthetics import *


# ═
equal_symbol = chr(9552)
# ═┳═
latteral_connection_symbol = chr(9552) + chr(9523) + chr(9552)
# ┗═
down_right_connection_symbol = chr(9495) + chr(9552)
# ⋘
triple_left_shift = chr(8920)
# ⋙
triple_right_shift = chr(8921)


# [
left_bracket_cyan = ConsoleColored("[", "cyan", bold=1)
# ]
right_bracket_cyan = ConsoleColored("]", "cyan", bold=1)


# -
dash_orange = ConsoleColored("-", "red", bold=1)


# <
left_arrow_blue = ConsoleColored("<", "blue", bold=1)
# <
left_arrow_yellow = ConsoleColored("<", "yellow", bold=1)
# >
right_arrow_blue = ConsoleColored(">", "blue", bold=1)
# >
right_arrow_yellow = ConsoleColored(">", "yellow", bold=1)

# >>>
left_arrow_3_green_bold = green_bold(">>>")