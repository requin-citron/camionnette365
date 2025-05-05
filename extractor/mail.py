from os              import path, getcwd
from extractor.utils import mkdir_if_exist

import requests

def get_message(access_token):
    message      = list()
    json_message = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages",
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()

    for msg in json_message["value"]:
        message.append((
            msg["id"],
            msg["hasAttachments"]
        ))
    
    return message

def download_message(access_token, id):
    content_mail = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{id}/$value", # id of email
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).content

    return content_mail

def get_attachment(access_token, id):
    attachement = list()
    json_attach = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{id}/attachments", # id of email
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).json()

    if json_attach.get("error") is None:

        for attach in json_attach["value"]:
            attachement.append((
                attach.get("id"),
                attach.get("name"),
            ))
    
    return attachement

def download_attachment(access_token, idmail, idattach):
    content_attach = requests.get(
        f"https://graph.microsoft.com/v1.0/me/messages/{idmail}/attachments/{idattach}/$value", # id of email, id of attachment
        headers={'Authorization': 'Bearer ' + access_token},
        timeout=30,
    ).content

    return content_attach


def dump_mail(access_token, user, extract_dir, debug=False):
    extract_path = path.join(getcwd(), extract_dir, "mail",user.replace("..",""))
    mkdir_if_exist(extract_path)
    
    for msg in get_message(access_token):
        id       = msg[0]
        content  = download_message(access_token, id)
        tmp_path = path.join(extract_path, id)

        mkdir_if_exist(tmp_path)
        open(path.join(tmp_path,"mail"),"wb").write(content)
        if debug:
            print(f"Mail : {id}")

        # attachment
        if msg[1]: # hasattachment ?
            for attach in get_attachment(access_token,id):
                content = download_attachment(access_token, id, attach[0])
                open(path.join(tmp_path,attach[1].replace("..","")),"wb").write(content)
                if debug:
                    print(f"Mail Attach : {attach[1].replace('..','')}")
