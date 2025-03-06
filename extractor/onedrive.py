from os                   import path, getcwd
from extractor.utils      import mkdir_if_exist

import requests

def parse_json_file(json_data):
    files = list()
    for data in json_data["value"]:
        files.append(
            (
                data["id"],
                data["name"],
                data["folder"]["childCount"] if data.get("folder") is not None else None,
            )
        )
    return files

def get_root(access_token):
    json_files = requests.get(
        f"https://graph.microsoft.com/v1.0/me/drive/root/children",
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()
    
    return parse_json_file(json_files)

def get_files(access_token,id=None):
    files      = list()
    json_files = requests.get(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{id}/children", # id of folder
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()

    return parse_json_file(json_files)

def download_files(access_token,id=None):
    content_file = requests.get(
        f"https://graph.microsoft.com/v1.0/me/drive/items/{id}/content", # id of file
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).content

    return content_file

def test(access_token):
    json_files = requests.get(
        f"https://graph.microsoft.com/v1.0/me/drive/items/01KMV5OAQFOSYSJRVO2JH2TPX5TGBP7I6T/children",
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()

    return json_files

def rec_download(access_token, files, fullpath, debug=False):
    dl_files      = [x for x in files if x[2] is None]
    dirs          = [x for x in files if x[2] is not None]
    non_empty_dir = [x for x in dirs  if x[2]>0]

    for d in dirs: # create dir
        mkdir_if_exist(path.join(fullpath, d[1].replace("..","") ))

    for f in dl_files: # dl file
        open(path.join(fullpath,f[1].replace("..","")), "wb").write(download_files(access_token, f[0]))
        
        if debug:
            print(f"OneDrive : {f[1].replace("..","")}")
    
    for d in non_empty_dir:
        rec_download(access_token, get_files(access_token, d[0]), path.join(fullpath, d[1].replace("..","")))

def dump_onedrive(access_token, user, extract_dir, debug=False):
    extract_path = path.join(getcwd(), extract_dir, "onedrive",user.replace("..",""))
    mkdir_if_exist(extract_path)
    rec_download(access_token, get_root(access_token), extract_path, debug) # rec download