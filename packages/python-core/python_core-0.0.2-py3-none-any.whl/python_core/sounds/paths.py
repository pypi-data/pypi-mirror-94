

# core package (pip install python-core)
from core.system import get_os

op_sys = get_os()

sounds_remote_path = None
if op_sys == "Windows":
    sounds_remote_path = "C:/Users/{username}/sounds/{type}"
elif op_sys == "Linux":
    sounds_remote_path = "/home/{username}/sounds/{type}"
elif op_sys == "Darwin":
    sounds_remote_path = "/Users/{username}/sounds/{type}"

del op_sys