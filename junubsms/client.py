import requests

from .base import BASE_URL
from .exceptions import JunubSMSError
from .messages import MessagesResource
from .admin import AdminResource


class JunubSMSClient:
    
    #Python client for the JunubSMS web API.
    def __init__(self, username: str, token: str = "", timeout: int = 30):
        self._username = username
        self._token = token
        self._session = requests.Session()
        self._session.headers.update({"Accept": "application/json"})

        self.messages = MessagesResource(username, token, self._session)
        self.admin = AdminResource(username, token, self._session)

    @classmethod
    def from_credentials(cls, username: str, password: str) -> "JunubSMSClient":
        #Authenticate with a username and password to fetch an API token
        #For use when you don't have a token yet.
        
        token = cls._fetch_token(username, password)
        return cls(username=username, token=token)

    @staticmethod
    def _fetch_token(username: str, password: str) -> str:
        #Call get_token and return the raw token string.
        response = requests.get(
            BASE_URL,
            params={"app": "ws", "op": "get_token", "u": username, "p": password, "format": "json"},
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        error = data.get("error_string") or data.get("status", "")
        if isinstance(error, str) and error.startswith("ERR"):
            raise JunubSMSError(code=error)

        return data.get("data", {}).get("h", "")

    def close(self):
        #Close the underlying HTTP session
        self._session.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
