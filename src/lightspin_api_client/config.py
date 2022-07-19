import ast
import json
import os

from lightspin_api_client.logger import Logger


class Config:
    _config_location = "config.json"

    def __init__(self):
        self.logger = Logger("config").logger
        if os.path.exists(self._config_location):
            self.logger.info("loading config from JSON file...")
            self.__dict__ = json.load(open(self._config_location))
        else:
            self.logger.info("loading config fron ENV...")
            self.log_level = os.environ["LOG_LEVEL"]

            # lightspin config
            self.lightspin_params_dict = os.environ["LIGHTSPIN_PARAMS_DICT"]
            self.lightspin_url = ast.literal_eval(os.environ["LIGHTSPIN_URL"])
            self.lightspin_username = os.environ["LIGHTSPIN_USERNAME"]
            self.lightspin_password = os.environ["LIGHTSPIN_PASSWORD"]

            # elastic config
            self.index_name_prefix = os.environ["INDEX_NANE_PREFIX"]
            self.elastic_hosts = ast.literal_eval(os.environ["ELASTIC_HOSTS"])
            self.elastic_user = os.environ["ELASTIC_USER"]
            self.elastic_password = os.environ["ELASTIC_PASSWORD"]
            self.elastic_transmit_chunk_size = int(
                os.getenv("ELASTIC_TRANSMIT_CHUCK_SIZE", 1000)
            )
            self.elastic_transmit_request_timeout = int(
                os.getenv("ELASTIC_TRANSMIT_REQUEST_TIMEOUT", 200)
            )

            # azure sentinel config
            self.laws_primary_agent_key = os.environ["LAWS_PRIMARY_AGENT_KEY"]
            self.laws_workspace_id = os.environ["LAWS_WORKSPACE_ID"]
            self.log_type = os.environ["LOG_TYPE"]

            # datadog config
            self.dd_api_key = os.environ["DD_API_KEY"]
            self.dd_site = os.environ["DD_SITE"]

            # google chronicle config
            self.api_key = os.environ["API_KEY"]

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return
