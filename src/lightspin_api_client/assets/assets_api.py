from urllib.parse import urlencode, urljoin

from lightspin_api_client.api import Api
from lightspin_api_client.logger import Logger


class AssetsApi(Api):
    def __init__(self, server_prefix, username, password, params_dict):
        super().__init__(server_prefix, username, password, params_dict)
        self.logger = Logger("assets_api").logger

    def get_assets_results(self):
        all_results = []
        endpoint = "api/useraction/assets"
        if self.params_dict:
            endpoint += "?" + urlencode(self.params_dict, doseq=True)
        url = urljoin(self.server_prefix, endpoint)
        self.logger.info(f"getting assets results from {url} ...")
        for results_list in self.results_generator(url):
            all_results.extend(results_list)
        self.logger.info(f"got {len(all_results)} assets results...")
        return all_results
