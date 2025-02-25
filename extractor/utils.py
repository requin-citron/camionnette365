from os import path, mkdir

def mkdir_if_exist(fullpath):
    if not path.exists(fullpath):
        mkdir(fullpath)