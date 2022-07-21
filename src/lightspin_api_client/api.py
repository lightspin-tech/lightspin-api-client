import requests
from .jwt import JwtTokens
from lightspin_api_client.logger import Logger

page_size = 200


class Api:
    def __init__(self, server_prefix, username, password, params_dict):
        self.logger = Logger("api").logger
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self.server_prefix = server_prefix
        self.username = username
        self.password = password
        self.params_dict = params_dict
        self.jwt_tokens = JwtTokens(server_prefix, username, password)
        self.headers["Authorization"] = f"JWT {self.jwt_tokens.jwt_access_token}"

    def results_generator(self, url) -> list:
        response = requests.get(url, headers=self.headers).json()
        yield response["results"]
        while True:
            next_page = response["next"]
            if not next_page:
                break
            try:
                self.logger.info(f"getting next page: {next_page}")
                response = requests.get(next_page, headers=self.headers).json()
                yield response["results"]
            except KeyError:
                self.logger.error(
                    "Failed to get results from response, trying again after refreshing the JWT tokens"
                )
                self.jwt_tokens.refresh_jwt_access_token()
                self.headers[
                    "Authorization"
                ] = f"JWT {self.jwt_tokens.jwt_access_token}"
            except Exception as e:
                self.logger.error(e)
                break
