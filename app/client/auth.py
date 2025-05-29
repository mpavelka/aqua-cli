import base64
from dataclasses import dataclass
import time
import hmac
import hashlib
import requests
import json


@dataclass
class AuthContext:
    token: str


def ensure_auth(token_file_path):
    print(f"Ensuring authentication using token file: {token_file_path}")
    try:
        with open(token_file_path, "r") as token_file:
            token_file_contents = token_file.read().strip()
            token_payload_b64 = token_file_contents.split(".")[1]
            token_payload_str = base64.b64decode(token_payload_b64 + "==").decode(
                "utf-8"
            )
            token = json.loads(token_payload_str)
            exp = token["exp"]

            # If the token is valid, authentication is successful
            if exp and time.time() < exp:
                return AuthContext(token=token_file_contents)

    except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
        print(f"Error loading token: {e}")


def authenticate(api_key, api_secret, token_file_path, ca_cert=None):

    # Generate timestamp
    timestamp = str(int(time.time()))

    # Define endpoint and method
    endpoint = "https://eu-1.api.cloudsploit.com/v2/tokens"
    method = "POST"

    # Define the body of the POST request
    post_body = {"validity": 20*60, "allowed_endpoints": ["GET"]}
    post_body_json = json.dumps(post_body, separators=(",", ":")).strip()

    # Create the string to sign
    string_to_sign = f"{timestamp}{method}/v2/tokens{post_body_json}"

    # Create HMAC signature
    signature = hmac.new(
        api_secret.encode("utf-8"),
        string_to_sign.encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()

    # Set headers
    headers = {
        "Content-Type": "application/json",
        "X-API-Key": api_key,
        "X-Timestamp": timestamp,
        "X-Signature": signature,
    }

    # Make the request
    response = requests.post(
        endpoint,
        headers=headers,
        data=post_body_json,
        verify=ca_cert if ca_cert else True,
    )

    # Parse the response
    if response.status_code == 200:
        print("Login successful.")
        token = response.json().get("data")
        # Store token to token_file_path
        with open(token_file_path, "w") as token_file:
            token_file.write(token)
        print(f"Token saved to {token_file_path}")
        # Store the parsed token payload into the token_file_path.json
        token_payload = json.loads(
            base64.b64decode(token.split(".")[1] + "==").decode("utf-8")
        )
        with open(token_file_path + ".json", "w") as token_file_json:
            json.dump(token_payload, token_file_json, indent=4)
        return token
    else:
        print(f"Authentication failed. Status: {response.status_code}")
        print("Response:", response.text)
        return None
