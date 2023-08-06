
"""
    core/__winapi.py
    useful windows api file

    author:@alexzander
"""


# 3rd party
from win10toast import ToastNotifier # pip install win10toast


def windows_notification(title, message, duration, icon, threaded=True):
    ToastNotifier().show_toast(title=title, msg=message, duration=duration, icon_path=icon, threaded=threaded)



# TESTING
if __name__ == '__main__':
    pass