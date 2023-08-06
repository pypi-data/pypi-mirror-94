

# python
from getpass import getuser
# core
from core.__path import *
# core/sounds
from core.sounds.paths import sounds_remote_path
from core.sounds.update import UpdateSounds


def create_remote_database(remote_path: str,
               original_remote_folder: str, 
               modified_remote_folder: str, 
               remote_sounds_json_path: str, 
               type: str):
    """ creation of sounds files and folder for the first time """
    # reseting everything
    if exists(remote_path):
        delete_folder(remote_path)
    # creating folders
    if not exists(original_remote_folder):
        os.makedirs(original_remote_folder)
    if not exists(modified_remote_folder):
        os.makedirs(modified_remote_folder)
    
    # copy the files from type/original to C:/Users/$username/sounds/$type/original
    sep = get_path_sep(__file__)
    original_folder = sep.join(__file__.split(sep)[:-1]) + f"/{type}/original"
    
    __sounds = os.listdir(original_folder)
    for s in __sounds:
        copy_file(original_folder + sep + s, original_remote_folder + sep + s, __print=True)
    
    # after creating the folders for the first time
    # also create the modified sounds
    # in order to be ready with everything
    UpdateSounds(
        original_remote_folder,
        modified_remote_folder,
        remote_sounds_json_path
    )


def check_remote_database(__type: str):
    sounds_folder = sounds_remote_path.format(username=getuser(), type=__type)

    # remote audio folders
    original_remote_folder = sounds_folder + "/original"
    modified_remote_folder = sounds_folder + "/modified"

    # remote database
    remote_sounds_json_path = sounds_folder + "/sounds.json"

    if  not exists(sounds_folder) or \
        is_folder_empty(sounds_folder) or \
        not exists(original_remote_folder) or \
        is_folder_empty(original_remote_folder) or \
        not exists(modified_remote_folder) or \
        is_folder_empty(modified_remote_folder) or \
        not exists(remote_sounds_json_path) or \
        is_file_empty(remote_sounds_json_path):
        
        # if one of the statements is true
        # then initialize everytime
        create_remote_database(
            sounds_folder,
            original_remote_folder, 
            modified_remote_folder,
            remote_sounds_json_path,
            __type
        )
    
    return remote_sounds_json_path