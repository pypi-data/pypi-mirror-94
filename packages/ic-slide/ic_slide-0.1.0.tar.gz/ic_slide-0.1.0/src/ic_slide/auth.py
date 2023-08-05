from .config import AuthUri
import json
import requests
import datetime
import logging
from getpass import getpass
logger = logging.Logger(__name__)

GRANT_TYPE = "password"
SCOPE = "AlgorithmService StorageIndex SlideCloudStorage AuthServer"
CLIENT_ID = "coriander"
CLIENT_SECRET = "secret"

USERNAME = input("Please enter the user name of coriander: ")
PASSWORD = getpass(f"Please enter the password of {USERNAME}: ")

_access_token = None
_request_access_token_time = datetime.datetime.now()
_access_expires_in = 3600


def urljoin(*args):
    """
    Joins given arguments into an url. Trailing but not leading slashes are
    stripped for each argument.
    """
    return "/".join(map(lambda x: str(x).rstrip('/'), args))


def _request_new_access_token():
    token_url = urljoin(AuthUri, 'connect/token')
    response = requests.post(token_url, data={
        "grant_type": GRANT_TYPE,
        "scope": SCOPE,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "username": USERNAME,
        "password": PASSWORD
    })
    if response.status_code >= 200 and response.status_code <= 299:
        content = json.loads(response.content)
        if 'access_token' not in content:
            raise ValueError(f"Invalid access token in content {content}")
        if 'scope' not in content:
            raise ValueError(f"Invalid scope in content {content}")
        if 'token_type' not in content:
            raise ValueError(f"Invalid token_type in content {content}")
        if 'expires_in' not in content:
            raise ValueError(f"Invalid expires_in content {content}")
    else:
        raise Exception(
            f"Can not get access token, because {response.reason} {response.content}")
    access_token = content['access_token']
    scope = content['scope']
    token_type = content['token_type']
    expires_in = int(content['expires_in'])

    return access_token, expires_in


def _is_valid_access_token():
    now = datetime.datetime.now()
    global _request_access_token_time
    global _access_token
    global _access_expires_in
    expires_time = _request_access_token_time + \
        datetime.timedelta(0, _access_expires_in)
    return _access_token != None and expires_time > now


def get_access_token():
    global _access_token
    global _access_expires_in
    global _request_access_token_time
    if not _is_valid_access_token():
        logger.info(f"requesting new access token")
        _access_token, _access_expires_in = _request_new_access_token()
        _request_access_token_time = datetime.datetime.now()
        logger.info(
            f"requested new access token, expires in {_access_expires_in}")
    return _access_token
