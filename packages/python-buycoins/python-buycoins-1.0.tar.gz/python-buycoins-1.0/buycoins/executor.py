import json
from typing import Any, Dict, List, Optional

import requests
from decouple import config
from requests.auth import HTTPBasicAuth
from requests.exceptions import ConnectionError

base_url = "https://backend.buycoins.tech/api/graphql"


class Executor:
    def __init__(
        self,
        username: str = config("PUBLIC_KEY"),
        password: str = config("PRIVATE_KEY"),
    ) -> None:
        self.username = username
        self.password = password

    def query(
        self, query: str, variables: Dict[str, str] = None
    ) -> Dict[str, Any]:
        try:
            results = requests.post(
                base_url,
                json={"query": query, "variables": variables},
                auth=HTTPBasicAuth(self.username, self.password),
            )
        except ConnectionError as error:
            return error
        else:
            if results.text == "":
                return {"data": None, "message": "Empty response!"}

            return results.json()
