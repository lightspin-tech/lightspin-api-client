# The Lightspin Python library

This Python library contains helpers and samples for Lightspin APIs.
Upon installation, the library helpers can be used to consume the API with built-in JWT authentication, paging and dynamic API parameters usage.

## Usage - SIEM API example
```bash
from lightspin_api_client.config import Config
from lightspin_api_client.logger import Logger
from lightspin_api_client.siem.siem_api import SiemApi

config = Config()
logger = Logger("siem_example").logger
siem_api = SiemApi(
    config.lightspin_url,
    config.lightspin_username,
    config.lightspin_password,
    config.lightspin_params_dict,
)
siem_results = siem_api.get_siem_results()
```

## Configuration JSON sample ([Elasticsearch](https://elasticsearch-py.readthedocs.io/))
```bash
{
  "log_level": "DEBUG",
  "elastic_user": "elastic",
  "elastic_password": "elastic",
  "elastic_hosts": [
    "1.2.3.4:8000"
  ],
  "lightspin_url": "https://id-123.lightspin.cloud",
  "lightspin_username": "light",
  "lightspin_password": "password1",
  "lightspin_params_dict": {
	"account_id": ["123"]
  },
  "index_name_prefix": "siem"
}
```

## Q&A
**Q: How does it speed up my work with the lightspin API?**
A: this library is taking care of authentication and paging for you so you don't have to.
It will also make sure you use the right API endpoints and body parameters.
So eventually you only to develop your own logics, and we'll take care of Lightspin's side for you. 

**Q: which SDK samples are provided?** 
A: Currently we provide 4 SIEM API samples:
1. [Splunk](https://github.com/lightspin-tech/lightspin-api-client/tree/main/src/lightspin_api_client/siem/splunk)
2. [Datadog](https://github.com/lightspin-tech/lightspin-api-client/tree/main/src/lightspin_api_client/siem/datadog)
3. [Elasticsearch](https://github.com/lightspin-tech/lightspin-api-client/tree/main/src/lightspin_api_client/siem/elastic)
4. [Azure Sentinel](https://github.com/lightspin-tech/lightspin-api-client/tree/main/src/lightspin_api_client/siem/azure_sentinel)

In the future we will also share samples for other public lightspin APIs.

### Contact Us
This library is developed by the Lightspin engineering group.
For more information, contact us at support@lightspin.io.

### License
This repository is available under the [MIT License](https://github.com/lightspin-tech/lightspin-api-client/blob/main/LICENSE).
