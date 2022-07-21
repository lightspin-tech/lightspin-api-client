import json

from lightspin_api_client.config import Config
from lightspin_api_client.logger import Logger
from lightspin_api_client.siem.siem_api import SiemApi


def main():
    config = Config()
    logger = Logger("splunk").logger
    siem_api = SiemApi(
        config.lightspin_url,
        config.lightspin_username,
        config.lightspin_password,
        config.lightspin_params_dict,
    )
    siem_results = siem_api.get_siem_results()
    logger.info("printing SIEM results to STDOUT")
    print(json.dumps(siem_results))


if __name__ == "__main__":
    main()
