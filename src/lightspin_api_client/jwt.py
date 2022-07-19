import requests
from urllib.parse import urljoin

from lightspin_api_client.logger import Logger


class JwtTokens:
    def __init__(self, server_prefix, username, password):
        self.logger = Logger("siem_api").logger
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.server_prefix = server_prefix
        self.jwt_access_token = None
        self.jwt_refresh_token = None
        self.create_jwt_tokens(username, password)

    def create_jwt_tokens(self, username, password):
        self.logger.info("creating JWT tokens...")
        endpoint = "auth/jwt/create/"
        if not username or not password:
            self.logger.info("missing lightspin credentials")
        payload = {"username": username, "password": password}
        url = urljoin(self.server_prefix, endpoint)
        try:
            response = requests.post(url, headers=self.headers, json=payload).json()
            try:
                self.jwt_access_token, self.jwt_refresh_token = (
                    response["access"],
                    response["refresh"],
                )
            except KeyError:
                msg = f"failed to get JWT tokens from response: '{response}'"
                self.logger.error(msg)
                raise IOError(msg)
        except Exception as e:
            msg = f"failed to create JWT tokens from URL: {url}"
            self.logger.error(msg)
            self.logger.exception(e)
            raise IOError(msg)

    def refresh_jwt_access_token(self):
        self.logger.info("refreshing JWT tokens...")
        endpoint = "auth/jwt/refresh/"
        payload = {"refresh": self.jwt_refresh_token}
        url = urljoin(self.server_prefix, endpoint)
        response = requests.post(url, headers=self.headers, json=payload).json()
        try:
            self.jwt_access_token = response["access"]
        except KeyError:
            raise IOError(f"Failed to get JWT tokens from response: '{response}'")
        self.logger.info("refreshed JWT tokens successfully!")

    def verify_jwt_token(self):
        self.logger.info("verifying JWT tokens...")
        endpoint = "auth/jwt/verify/"
        payload = {"token": self.jwt_access_token}
        url = urljoin(self.server_prefix, endpoint)
        response = requests.post(url, headers=self.headers, json=payload).json()
        if response.get("code") == "token_not_valid":
            self.logger.info("JWT token isn't valid")
            return False
        self.logger.info("JWT token is valid")
        return True
