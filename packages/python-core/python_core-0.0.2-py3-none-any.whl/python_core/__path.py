
"""
    core/__path.py

    useful module in development of programs
    that work with paths

    author: @alexzander
"""


# python
import os
from time import sleep
from string import ascii_lowercase

# core package (pip install python-core)
from core.system import *
from core.aesthetics import *
from core.exceptions import *

# 3d party
from win32com.client import Dispatch # pip install pywin32


# no matter what os you have
# / (slash) is the best on all platforms
# and also
# op_sys = get_os()
# if op_sys == "Windows":
#     separator__ = "\\"
separator__ = "/"
# SEPARATOR \\ IS FORBIDDEN !!!!


win_drive_letters__ = [letter + ":" for letter in ascii_lowercase]
illegal_chars__ = ":*?\"<>|"


class __path_Exception(Exception):
    """
        __path (name of this file)
        _Exception
        means this is a exception super class
        for this file only
    """
    def __init__(self, message=""):
        self.message = message


class InvalidPathError(__path_Exception):
    pass


class InvalidExtensionError(__path_Exception):
    pass


class IncorrectExtensionError(__path_Exception):
    pass


class IllegalPathError(__path_Exception):
    pass


class DifferentExtensionsError(__path_Exception):
    pass


class ContainsNoSeparatorError(__path_Exception):
    pass


class NotAFileError(__path_Exception):
    pass


class NotAFolderError(__path_Exception):
    pass


def get_path_sep(path: str):
    """ return path separator (\\ or /) from @path """
    back_slashes = path.count("\\")
    slashes = path.count("/")
    if (back_slashes == 0 and slashes > 0) or (back_slashes > 0 and slashes > 0):
        return "/"
    elif back_slashes > 0 and slashes == 0:
        return "\\"
    elif back_slashes == 0 and slashes == 0:
        raise IllegalPathError("path: {} doesnt contain any (\\) or (/)".format(red_bold(path)))


def is_valid_path(path: str):
    """ shouldnt exist, must contain separators """
    op_sys = get_os()
    if op_sys == "Windows":
        back_slashes = path.count("\\")
        slashes = path.count("/")
        if back_slashes == 0 and slashes == 0:
            # doesnt contain path separator
            return False

        # beginning = path[:2].lower() # (C:) only
        # if beginning not in drive_letters__:
        #     # doesnt start with valid windows drive letter
        #     return False
        # if path[3] != "\\" and path[3] != "/":
        #     # doesnt start with separator after drive letter
        #     return False
        for char in path[4:]:
            if char in illegal_chars__:
                return False

    elif op_sys == "Linux" or op_sys == "Darwin":
        slashes = path.count("/")
        if slashes == 0:
            return False
        for char in path:
            if char in illegal_chars__:
                return False

    return True


def get_path_from_absolute(path: str):
    """ extracts the path from @src

        "folder1/folder2/folder3/folder4/file_name.extension" =>
        => "folder1/folder2/folder3/folder4"
    """

    # validation
    if type(path) != str:
        raise TypeError
    if not is_valid_path(path):
        raise InvalidPathError
    # /validation

    if get_path_sep(path) == "\\":
        return separator__.join(path.split("\\")[:-1])
    return separator__.join(path.split(separator__)[:-1])


def is_file(path: str):
    """ should exist on disk and should be a avalid file path format """
    return os.path.isfile(path)


def is_folder(path: str):
    """ should exist on disk and should be a valid folder path format """
    return os.path.isdir(path)


def is_folder_empty(path: str):
    """ tests whether the @source_folder is empty or not """

    # validation
    if type(path) != str:
        path = str(path)
    if not is_folder(path):
        raise NotAFolderError
    # /validation
    return os.listdir(path) == 0


def is_file_empty(path: str):
    if not is_file(path):
        raise NotAFileError

    try:
        content = open(path, "r+").read()
        if content == "ÿþ" or content == "":
            return True
    except Exception as error:
        print(error)
        print(error.message)
        print(type(error))

    return False


def is_abs(path: str):
    """ doesnt need to exist and should be a valid folder or file path format """
    return os.path.isabs(path)


def exists(path: str):
    """ should exist and should be a valid folder folder or file path format """
    return os.path.exists(path)


def delete_last_slash(path: str):
    """ gets [
            'folder1\folder2\folder3\'
                        or
            'folder1/folder2/folder3/'
        ]
        return 'folder1\folder2\folder3
    """
    if path.endswith("\\") or path.endswith("/"):
        # modification through reference
        path = path[:-1]


def get_file_name(path: str):
    """ gets 'folder1/folder2/folder3/file_name.extension"
        return file_name
    """

    # validation
    if type(path) != str:
        path = str(path)
    if not is_valid_path(path):
        raise InvalidPathError
    # /validation

    sep = get_path_sep(path)

    if "." not in path:
        return path.split(sep)[-1]

    # noisnetxe.eman_elif (file_name.extension revered)
    # it can contain multiple '.' (dots) and that is confusing
    full_file_name_rev = path.split(sep)[-1][::-1]

    # from the first '.' to the end, reversed
    return full_file_name_rev[full_file_name_rev.index(".") + 1: ][::-1]


def get_file_extension(path: str):
    """ gets 'folder1/folder2/folder3/folder4/file_name.extension'
        return 'extension'
    """

    # validation
    if type(path) != str:
        path = str(path)
    if not is_valid_path(path):
        raise InvalidPathError
    if "." not in path:
        raise ValueError("there is no '.' (dot) in the @path - [this file has no extension]")
    # /validation

    # noisnetxe.eman_elif (file_name.extension reversed)
    path_rev = path[::-1]
    i = path_rev.find(".")
    return path_rev[:i][::-1]


def get_filename_plus_extension(path: str):
    """ gets 'folder1/folder2/folder3/folder4/file_name.extension'
        return 'file_name.extension'
    """

    # validation
    if type(path) != str:
        path = str(path)
    if not is_valid_path(path):
        raise InvalidPathError
    # /validation

    return path.split(get_path_sep(path))[-1]


from core.drive import *


class File:
    def __init__(self, path: str):
        if not is_valid_path(path):
            raise InvalidPathError

        self.path = path
        self.cwd = get_path_from_absolute(path)
        self.name = get_file_name(path)
        self.extension = get_file_extension(path)
        self.name_plus_extension = get_filename_plus_extension(path)
        self.sep = get_path_sep(path)

        if is_file(path):
            self.size_in_bytes = get_size_in_bytes(path)


class Folder:
    def __init__(self, path: str):
        if not is_valid_path(path):
            raise InvalidPathError

        self.path = path
        self.cwd = get_path_from_absolute(path)
        self.sep = get_path_sep(path)
        self.name = path.split(sep)[-1]

        if is_folder(path): # exists on disk
            self.size_in_bytes = get_size_in_bytes(path)


space_4  = " " * 4
branch = '│   '
tee    = '├───'
final  = '└───'

def tree_repr(folder: str, prefix=" " * 4):
    representation = ""

    __items = os.listdir(folder)
    pointers = [tee] * (len(__items) - 1) + [final]

    sep = get_path_sep(folder)
    for pointer, __item in zip(pointers, __items):
        full_path = folder + sep + __item
        representation += prefix + pointer + __item + "\n"
        if is_folder(full_path):
            extension = branch if pointer == tee else space_4
            representation += tree_repr(full_path, prefix + extension)

    return representation


def tree_representation(folder: str):
    if not is_folder(folder):
        raise NotAFolderError

    sep = get_path_sep(folder)
    result = tree_repr(folder)
    result = folder.split(sep)[-1] + " ( {} )\n".format(folder) + result
    return result




# TESTING
if __name__ == '__main__':
    pass