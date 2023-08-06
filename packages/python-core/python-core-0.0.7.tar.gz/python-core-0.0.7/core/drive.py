
"""
    core/drive.py

    useful in development of programs that
    involve work with the disk drive or any
    disk drive

    author: @alexzander
"""


# python
import os
import string
import threading
import subprocess
import multiprocessing
from time import time, sleep
from concurrent.futures import ThreadPoolExecutor

# core package (pip install python-core)
from core.system import *
from core.aesthetics import *
from core.exceptions import *
from core.__winapi import *
from core.__numbers import *
from core.__path import *

# 3rd party
from win32 import win32api # pip install pywin32


def transfer__(src: str, dst: str):
    """
        first: content is validated
        second: reads from @src in binary and writes in binary to @dst
    """

    # validation
    if not exists(src):
        raise FileNotFoundError
    if not is_file(src):
        raise NotAFileError
    if not exists(dst):
        path = get_path_from_absolute(dst)
        # if the file @dst doesnt exist
        # the folders path is created
        # except the name of the file
        # that is created below in the
        # copy 'with' statement
        os.makedirs(path, exist_ok=True)
    # /validation

    with open(src, "rb") as src_bin:
        # if the @dst file doesnt exist
        # is created automatically
        with open(dst, "wb") as dst_bin:
            # deleted existed content
            dst_bin.truncate(0)
            # replaced with brand-new one
            dst_bin.write(src_bin.read())


def copy_file(src: str, dst: str, __print=False):
    """ copys from source to destination (available only for FILES)
        return True (means that code was executed successfully)

        prints output of code=0 to the screen if __print
    """

    # path validation
    if not is_file(src):
        raise NotAFileError
    if not is_valid_path(dst):
        raise InvalidPathError
    # path /validation

    sep_src = get_path_sep(src)
    sep_dst = get_path_sep(dst)

    # extensions validation
    filename_src = src.split(sep_src)[-1] # filename
    filename_dst = dst.split(sep_dst)[-1] # filename
    if filename_src != filename_dst:
        # if the same is diff, means
        # tha they have different extenions
        raise DifferentExtensionsError("{}\n{}".format(filename_src, filename_dst))
    # /extensions validation

    # @dst folder should exist in the first place
    # after that you can copy the file successfully
    try:
        transfer__(src, dst)
    except PermissionError as error:
        print(error.message)
        print(error)
        print(type(error))
        return False
    except Exception as error:
        print_red_bold("something was wrong")
        print_red_bold(error)
        print_red_bold(type(error))
        return False

    if __print:
        print()
        print("[" + "=" * 50 + "]")
        print("source: {}".format(blue(src)))
        print("[~]")
        print("dest: {}".format(cyan(dst)))
        print("[~]")
        print(green_bold("file copied successfully!"))
        print("[" + "=" * 50 + "]")
        print()

    # code=0
    return True


def copy_folder(src: str, dst: str, __print=False, __folderignore=[]):
    """ copys from @source_folder to @destination_folder (available only for FOLDERS)

        prints output of code=0 to the screen if __print
    """

    # validation
    if not is_folder(src):
        raise NotAFolderError
    if not is_valid_path(dst):
        raise InvalidPathError
    # /validation

    sep_src = get_path_sep(src)
    sep_dst = get_path_sep(dst)

    # iterating through __items in that folder
    for __item in os.listdir(src):
        src_path = src + sep_src + __item
        dst_path = dst + sep_dst + __item

        if is_file(src_path):
            copy_file(src_path, dst_path, __print)
        elif is_folder(src_path):
            if __folderignore:
                if "" in __folderignore:
                    __folderignore = list(filter(lambda e: e != "", __folderignore))
                if __item in __folderignore:
                    continue

            copy_folder(src_path, dst_path, __print, __folderignore)

            if __print:
                print()
                print("[" + "=" * 50 + "]")
                print("source: {}".format(blue(src_path)))
                print("[~]")
                print("dest: {}".format(cyan(dst_path)))
                print("[~]")
                print(green_bold("folder copied successfully!"))
                print("[" + "=" * 50 + "]")
                print()

    # code=0
    return True


def create_shortcut(src: str, dst: str, __print=False):
    """
        creates shortcut of @src and puts it into
        @dst with name

        prints output of code=0 to the screen if __print
    """
    # params validation
    if not is_file(src):
        raise NotAFileError
    if not is_folder(dst):
        raise NotAFolderError
    # /params validation

    sep_src = get_path_sep(src)
    sep_dst = get_path_sep(dst)

    # current working folder
    cwd = sep_src.join(src.split(sep_src)[:-1])

    delete_last_slash(dst)

    # creation of shortcut
    shell = Dispatch("WScript.Shell")
    shortcut = shell.CreateShortcut(dst + sep_dst + get_file_name(src) + ".lnk")
    shortcut.TargetPath = src
    shortcut.WorkingDirectory = cwd
    shortcut.IconLocation = src
    shortcut.save()

    if __print:
        print()
        print("[" + "=" * 50 + "]")
        print("source: {}".format(blue(src)))
        print("[~]")
        print("destination: {}".format(cyan(dst)))
        print("[~]")
        print(green_bold("was made shortcut successfully!"))
        print("[" + "=" * 50 + "]")
        print()

    # code=0
    return True


def is_flash_drive(drive: str):
    """ checks if a drive is USB-drive or NOT """
    try:
        os.listdir(drive)
        return True
    except PermissionError:
        return False


def get_available_drives():
    """ gets all available drives """
    ops = get_os()
    if ops == "Windows":
        return win32api.GetLogicalDriveStrings().split("\000")[:-1]
    elif ops == "Linux":
        return os.listdir("/media")
    elif ops == "Darwin":
        return os.listdir("/Volumes")


def get_available_drives_non_usb():
    """ return all NON-USB drives that you can copy files to """
    return [dv for dv in get_available_drives() if is_flash_drive(dv)]


def open_folder(path: str):
    """ opens folder """

    # validation
    if not is_folder(path):
        raise NotAFolderError
    # /validation

    ops = get_os()
    if ops == "Windows":
        subprocess.Popen(["explorer.exe", path])
    elif ops == "Linux":
        os.system("xdg-open \"{}\"".format(path))
    elif ops == "Darwin":
        os.system("open \"{}\"".format(path))

def open_file(path: str):
    """ opens a file """

    # validation
    if not is_file(path):
        raise NotAFileError
    # /validation

    ops = get_os()
    if ops == "Windows":
        os.startfile(path)
    elif ops == "Linux":
        os.system("xdg-open \"{}\"".format(path))
    elif ops == "Darwin":
        os.system("open \"{}\"".format(path))

def delete_folder(path: str):
    """ deletes a folder """

    if not is_folder(path):
        raise NotADirectoryError

    try:
        ops = get_os()
        if ops == "Windows":
            os.system("rmdir /S /Q {}".format(path))
        elif ops == "Linux":
            os.system("rm -r {}".format(path))
        elif ops == "Darwin":
            os.system("rm -rf {}".format(path))
        return True
    except PermissionError as error:
        # system folder or another process is using it
        print(error.message)
        print(type(error))
        print(error)
        return False
    except Exception as error:
        print(error.message)
        print(type(error))
        print(error)
        return False


def extract_folders(file: str, path: str, curr_lvl=1, deep_lvl=2, __print=False):
    """
        function used to gather folders on different
        deepness level in order to maximize efficient in
        file searching on disk

        return => @extracted_folders, list of folder paths
            that will be helpful for creating a thread
            searching on that folder path for @file

        raise StopRecursive exception if file is found
    """

    # list with paths
    extracted_folders = []
    try:
        sep = get_path_sep(path)
        for item in os.listdir(path):
            full_path = path + sep + item

            if is_folder(full_path):
                if __print:
                    print_red(full_path)
                if curr_lvl < deep_lvl:
                    extracted_folders.extend(extract_folders(file, full_path, curr_lvl + 1, deep_lvl, __print))
                elif curr_lvl == deep_lvl:
                    extracted_folders.append(full_path)

            elif is_file(full_path):
                if file == item:
                    if __print:
                        print_green("\nfile found!\n")
                        print("located on: {}".format(blue_underlined(full_path)))
                    raise StopRecursive(full_path)
                else:
                    if __print:
                        print_red(full_path)

    except NotADirectoryError:
        if file == path.split(sep)[-1]:
            if __print:
                print_green_bold("\nfile found!\n")
                print("located on: {}".format(blue_underlined(path)))
            raise StopRecursive(path)

    except PermissionError:
        pass

    return extracted_folders


def find_file_on_drive(file: str, path: str, __threading=True, deep_lvl=1, __print=False):
    """
        if @__threading is True
            this function search the @file on many threads concurrently
            no. of threads == no. of folder in the @path folder

            it is recommended to have as many folders as possible in the @path folder
            otherwise if you have 3 folders means 3 threads and if you are searching in 1 TB of data
                its gonna take a while


        else
            searches recursively on a single thread (not recommended)

        if file was found
            return file_path
        else
            return False

    """
    if __threading:
        search_tasks = []
        try:
            extracted_folders = extract_folders(file, path, deep_lvl=deep_lvl, __print=__print)
        except StopRecursive as result:
            # we found the file before
            # creating the search threads
            return result.message

        max_workers = len(extracted_folders)
        for path in extracted_folders:
            search_tasks.append((__find_file_on_drive, [file, path, __print]))

        if __print:
            print()
            for task in search_tasks:
                print(task)
            print("\nThere are [ {} ] threads prepared for execution.\n".format(red_bold(len(search_tasks))))

            choice = input("proceed? [y/n]:\n")
            if choice != "y":
                return red_bold("finding-process-canceled")

            print_yellow_bold("\nsearching...\n")

            before = None

        try:
            workers_results = []
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                if __print:
                    before = time()

                for task in search_tasks:
                    workers_results.append(executor.submit(task[0], *task[1]))

                for wr in workers_results:
                    wr = wr.result()
                    if wr != None and is_abs(wr):
                        if __print:
                            after = time() - before
                            after = fixed_set_precision_str(after, 2)
                            print("from thread-pool")
                            print("execution time: [ {} seconds(s) ]".format(yellow_bold(after)))
                        return wr

        except StopRecursive as result:
            if __print:
                after = time() - before
                after = fixed_set_precision_str(after, 2)
                print("from exception")
                print("execution time: [ {} seconds(s) ]".format(yellow_bold(after)))
            return result.message

    else:
        # non-threaded version (ignore)
        try:
            __find_file_on_drive(file, path, __print)
        except StopRecursive as result:
            return result.message

    # file was not found on the entire disk
    # case 1: it doesnt exist
    # case 2: file name is incorrectly provided
    return False


def __find_file_on_drive(file: str, path: str, __print=False):
    try:
        sep = get_path_sep(path)
        for item in os.listdir(path):
            full_path = path + sep + item

            if is_folder(full_path):
                if __print:
                    print_red(full_path)
                __find_file_on_drive(file, full_path, __print)

            elif is_file(full_path):
                if file == item:
                    if __print:
                        print_green(full_path)
                        print_green_bold("\n\nfile found!")
                        print("located on: {}\n\n".format(blue_underlined(full_path)))
                    raise StopRecursive(full_path)
                else:
                    if __print:
                        print_red(full_path)

    except NotADirectoryError:
        if file == path.split(sep)[-1]:
            print_green_bold("\nfile found!\n")
            print("located on: {}".format(blue_underlined(path)))

    except PermissionError:
        # this is a system folder
        # or another process is using this
        # file or folder
        pass

def get_size_in_bytes(path: str):
    size = 0
    if is_file(path):
        size += os.path.getsize(path)

    elif is_folder(path):
        sep = get_path_sep(path)
        for __item in os.listdir(path):
            size += get_size_in_bytes(path + sep + __item)

    return size


chunk_size = 1000
digital_units = ["KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]

def convert_size_in_bytes(size):
    """
        return tuple (
            size,
            digital measurement unit for size
        )
    """
    if size < chunk_size:
        return size, "bytes"

    index = -1
    while (size % chunk_size) != size:
        size //= chunk_size
        index += 1

    return size, digital_units[index]


def get_size_on_disk(path: str):
    """
        return tuple (
            size,
            digital measurement unit for size
        )
    """
    return convert_size_in_bytes(get_size_in_bytes(path))





# TESTING
if __name__ == '__main__':
    pass