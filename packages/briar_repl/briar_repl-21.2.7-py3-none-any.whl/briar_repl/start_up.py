import os
import errno
import getpass
from pathlib import Path
import colorful as col
from dataclasses import dataclass
from .__init__ import __version__


@dataclass
class App:
    version : str  = __version__
    name    : str  = "briar_repl"


def get_auth_token():
    AUTH_FILE = Path(f"/home/{getpass.getuser()}/.briar/auth_token")
    if not AUTH_FILE.exists():
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), AUTH_FILE)
    with open(AUTH_FILE) as txt:
        token = txt.read().strip()
        return {'Authorization': f'Bearer {token}'}, token


APP = App()
AUTH, TOKEN = get_auth_token()
HOST = "127.0.0.1"
PORT = 7000
API_VERSION = "v1"
URL_BASE = f'http://{HOST}:{PORT}/{API_VERSION}/'
print(f"\nwelcome to {col.bold_chartreuse(APP.name)}!")
print("to list all functionality enter 'help'.\n")

URLS = {
    "BASE"            : URL_BASE,
    "CONTACTS"        : f"{URL_BASE}contacts",
    "CONTACTS_PENDING": f"{URL_BASE}contacts/add/pending",
    "ADD_LINK"        : f"{URL_BASE}contacts/add/link",
    "MSGS"            : f"{URL_BASE}messages/",
    "BLOGS"           : f"{URL_BASE}blogs/posts",
    "WS"              : f'ws://{HOST}:{PORT}/{API_VERSION}/ws',
}
