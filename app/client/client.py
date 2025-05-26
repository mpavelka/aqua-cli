from urllib.parse import urljoin
import requests

BASE_URL = "https://eu-central-1.edge.cloud.aquasec.com"
TOKEN_FILE_PATH = ""


class AquaSession(requests.Session):
    _auth_token: str | None = None
    _token_file_path: str | None = None

    def set_token_file_path(self, path):
        self._token_file_path = path

    def request(self, method, url, *args, **kwargs):
        url = urljoin(BASE_URL, url)
        headers = kwargs.get("headers", {})
        token = self._load_token()

        if token:
            headers.update({"Authorization": f"Bearer {token}"})

        kwargs["headers"] = headers
        request = super().request(method, url, *args, **kwargs)
        return request

    def _load_token(self):
        if self._token_file_path is None:
            return None

        try:
            with open(self._token_file_path, "r") as token_file:
                token_file_contents = token_file.read().strip()
                return token_file_contents

        except FileNotFoundError as e:
            print(f"Error loading token: {e}")
            return None


AquaClient = AquaSession()
