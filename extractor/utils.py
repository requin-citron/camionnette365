from os import path, makedirs

def mkdir_if_exist(fullpath):
    if not path.exists(fullpath):
        makedirs(fullpath)