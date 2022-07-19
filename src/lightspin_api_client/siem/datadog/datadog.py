# builtins imports
import json
import os
# datadog imports
from datadog_api_client.v2 import ApiClient, ApiException, Configuration
from datadog_api_client.v2.api.logs_api import LogsApi
from datadog_api_client.v2.model.content_encoding import ContentEncoding
from datadog_api_client.v2.model.http_log import HTTPLog
from datadog_api_client.v2.model.http_log_item import HTTPLogItem
# lightspin imports
from lightspin_api_client.config import Config
from lightspin_api_client.logger import Logger
from lightspin_api_client.siem.siem_api import SiemApi

config = Config()
os.environ['DD_API_KEY'] = config.dd_api_key
os.environ['DD_SITE'] = config.dd_site


def main():
    logger = Logger("datadog").logger
    siem_api = SiemApi(
        {config.lightspin_url},
        config.lightspin_username,
        config.lightspin_password,
        config.lightspin_params_dict,
    )
    siem_results = siem_api.get_siem_results()
    if not siem_results:
        logger.error("No siem results from lightspin, exiting...")
        exit()

    with ApiClient(Configuration()) as api_client:
        api_instance = LogsApi(api_client)
        try:
            body = HTTPLog(
                [
                    HTTPLogItem(
                        ddsource="lightspin",
                        ddtags="siem:lightspin",
                        hostname="lightspin",
                        message=json.dumps(r),
                        service="lightspin",
                    ) for r in siem_results
                ]
            )
            api_instance.submit_log(content_encoding=ContentEncoding("deflate"), body=body)
        except ApiException as e:
            logger.exception(f"API exception: '{e}'")
        except Exception as e:
            logger.exception(f"General Error: '{e}'")


if __name__ == "__main__":
    main()
