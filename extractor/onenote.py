from os         import path, getcwd
from app_config import EXTRACT_DIR
from extractor.utils      import mkdir_if_exist

import requests



def get_notebook(access_token):
    notebook      = list()
    json_notebook = requests.get(
        "https://graph.microsoft.com/v1.0/me/onenote/notebooks",
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()

    for data in json_notebook["value"]:
        notebook.append((data["displayName"], data["id"]))

    return notebook

def get_section(access_token, notebook_id):
    section      = list()
    json_section = requests.get(
        f"https://graph.microsoft.com/v1.0/me/onenote/notebooks/{notebook_id}/sections", # id of the notebook
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()

    for data in json_section["value"]:
        section.append((data["displayName"], data["id"]))

    return section

def get_page(access_token, section_id):
    page      = list()
    json_page = requests.get(
        f"https://graph.microsoft.com/v1.0/me/onenote/sections/{section_id}/pages", # id of the section
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()

    for data in json_page["value"]:
        page.append((data["title"], data["id"]))

    return page

def download_page(access_token, page_id):
    html_page = requests.get(
        f"https://graph.microsoft.com/v1.0/me/onenote/pages/{page_id}/content", # id of the page
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).text

    return html_page

def dump_onenote(access_token, user):
    extract_path = path.join(getcwd(), EXTRACT_DIR, "onenote",user.replace("..",""))
    mkdir_if_exist(extract_path)
    
    for notebook in get_notebook(access_token):
        tmp_path = path.join(extract_path, notebook[0].replace("..","")) # not the best way
        mkdir_if_exist(tmp_path)

        for section in get_section(access_token, notebook[1]):
            tmp_path_section = path.join(tmp_path, section[0].replace("..","")) # not the best way
            mkdir_if_exist(tmp_path_section)

            for page in get_page(access_token, section[1]):
                tmp_path_page = path.join(tmp_path_section, page[0].replace("..","")) # not the best way
                page_content  = download_page(access_token, page[1])
                open(tmp_path_page, "w").write(page_content)