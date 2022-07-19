# The Lightspin Python library

![PyPI - Version](https://img.shields.io/pypi/v/lightspin-api-client)
![PyPI - License](https://img.shields.io/pypi/l/lightspin-api-client)

This Python library contains helpers and samples for Lightspin APIs.
Upon installation, the library helpers can be used to consume the API with built-in JWT authentication, paging and dynamic API parameters usage.

## Installation:

```bash
pip3 install lightspin-api-client
```

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

## Configuration JSON sample
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

### Contact Us
This library is developed by the Lightspin engineering group.
For more information, contact us at support@lightspin.io.

### License
This repository is available under the [MIT License](https://github.com/lightspin-tech/lightspin-api-client/blob/main/LICENSE).