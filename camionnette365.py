#!/bin/python3
from base64             import b64decode
from colorama           import Fore
from datetime           import datetime
from extractor.mail     import dump_mail
from extractor.onedrive import dump_onedrive
from extractor.onenote  import dump_onenote
import argparse
import json

def color_string(string, color, flag):
    if not flag:
        return string
    return color + string + Fore.RESET


parser = argparse.ArgumentParser(description="Process access token, output directory, and optional flags.")

parser.add_argument("--access-token",   type=str, required=True, help="Access token for authentication.")
parser.add_argument("--outdir",         type=str, default=".",   help="Output directory path (default: current directory).")
parser.add_argument("--dump-mail",      action="store_true",     help="Enable dumping mail data.")
parser.add_argument("--dump-onedrive",  action="store_true",     help="Enable dumping OneDrive data.")
parser.add_argument("--dump-onenote",   action="store_true",     help="Enable dumping OneNote data.")
parser.add_argument("--show-tokeninfo", action="store_true",     help="Enable showing access token data.")
parser.add_argument("--color",          action="store_true",     help="Enable color output.")
parser.add_argument("--debug",          action="store_true",     help="debug.")

args = parser.parse_args()

try:
    access_token_data = args.access_token.split(".")[1]
    if len(access_token_data) % 4 != 0:
        access_token_data += "=" * (4 - (len(access_token_data) % 4))
    access_token_data = json.loads(b64decode(access_token_data))
except Exception as e:
    print(f"Error while decoding access token : {e}")
    exit(1)

#show token info
if args.show_tokeninfo:
    exp = datetime.fromtimestamp(access_token_data["exp"]).strftime('%Y-%m-%d %H:%M:%S')
    #print(json.dumps(access_token_data, indent=4))
    print(f"unique_name       : {color_string(access_token_data.get('unique_name',''),     Fore.CYAN,    args.color)}")
    print(f"expiration        : {color_string(exp,                                  Fore.MAGENTA, args.color)}")
    print(f"scope             : {color_string(access_token_data.get('scp',''),             Fore.MAGENTA, args.color)}")
    print(f"tenant id         : {color_string(access_token_data.get('tid', ''),             Fore.BLACK,   args.color)}")
    print(f"app id            : {color_string(access_token_data.get('appid', ''),           Fore.BLACK,   args.color)}")
    print(f"app name          : {color_string(access_token_data.get('app_displayname',''), Fore.BLACK,   args.color)}")

if args.dump_mail:
    dump_mail(args.access_token, access_token_data['unique_name'], args.outdir,     debug=args.debug)

if args.dump_onedrive:
    dump_onedrive(args.access_token, access_token_data['unique_name'], args.outdir, debug=args.debug)

if args.dump_onenote:
    dump_onenote(args.access_token, access_token_data['unique_name'], args.outdir,  debug=args.debug)
