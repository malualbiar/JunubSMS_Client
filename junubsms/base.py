import requests
from typing import Any, Dict, Optional

from .exceptions import JunubSMSError

BASE_URL = "https://sms.junubsms.com/index.php"


class BaseResource:

    #Shared HTTP logic for all resources.

    def __init__(self, username: str, token: str, session: requests.Session):
        self._username = username
        self._token = token
        self._session = session

    def _get(self, op: str, **params) -> Any:
        
        #Make a GET request and return the parsed JSON.
        
        query = {
            "app": "ws",
            "u": self._username,
            "h": self._token,
            "op": op,
            "format": "json",
            **{k: v for k, v in params.items() if v is not None},
        }

        response = self._session.get(BASE_URL, params=query, timeout=30)
        response.raise_for_status()

        data = response.json()
        self._check_for_errors(data)
        return data

    def _check_for_errors(self, data: Any) -> None:
        #Raise JunubSMSError if the response contains an error code.

        if not data:
            raise JunubSMSError("ERR 501")

        error_code = data.get("error_string")

        if isinstance(error_code, str) and error_code.startswith("ERR"):
            raise JunubSMSError(error_code)