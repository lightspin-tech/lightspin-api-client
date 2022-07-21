import json
import requests
import datetime
import hashlib
import hmac
import base64

from lightspin_api_client.config import Config
from lightspin_api_client.logger import Logger
from lightspin_api_client.siem.siem_api import SiemApi

logger = Logger("azure_sentinel").logger

api_version = "2016-04-01"
resource = "/api/logs"
uri_suffix = f".ods.opinsights.azure.com{resource}?api-version={api_version}"


def build_signature(date, content_length, content_type, config):
    sig_string = (
        "POST\n"
        + str(content_length)
        + "\n"
        + content_type
        + "\n"
        + f"x-ms-date:{date}"
        + "\n"
        + resource
    )
    logger.info(f"building signature from: {sig_string}")
    encoded_sig_string = bytes(sig_string, encoding="utf-8")
    decoded_laws_shared_key = base64.b64decode(config.laws_primary_agent_key)
    encoded_sig_hash = base64.b64encode(
        hmac.new(
            decoded_laws_shared_key, encoded_sig_string, digestmod=hashlib.sha256
        ).digest()
    ).decode()
    return f"SharedKey {config.laws_workspace_id}:{encoded_sig_hash}"


def post_data(body, content_type, signature, rfc1123date, config):
    uri = f"https://{config.laws_workspace_id}{uri_suffix}"
    headers = {
        "content-type": content_type,
        "Authorization": signature,
        "Log-Type": config.log_type,
        "x-ms-date": rfc1123date,
    }
    logger.info(f"posting SIEM results to {uri} with headers: {headers}")
    response = requests.post(uri, data=body, headers=headers)
    status_code = response.status_code
    if 200 <= status_code <= 299:
        logger.info(f"data accepted, status code: {status_code}")
    else:
        logger.error(f"failed to post data, error code: {status_code}")


def main():
    config = Config()
    siem_api = SiemApi(
        config.lightspin_url,
        config.lightspin_username,
        config.lightspin_password,
        config.lightspin_params_dict,
    )
    siem_results = siem_api.get_siem_results()
    content_type = "application/json"
    rfc1123date = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
    body = json.dumps(siem_results)
    signature = build_signature(rfc1123date, len(body), content_type, config)
    post_data(body, content_type, signature, rfc1123date, config)


if __name__ == "__main__":
    main()
