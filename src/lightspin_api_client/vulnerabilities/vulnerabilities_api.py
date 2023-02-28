from urllib.parse import urlencode, urljoin

from lightspin_api_client.api import Api
from lightspin_api_client.logger import Logger


class VulnerabilitiesApi(Api):
    def __init__(self, server_prefix, username, password, params_dict):
        super().__init__(server_prefix, username, password, params_dict)
        self.logger = Logger("vulnerabilities_api").logger

    def get_vulnerabilities_results(self):
        all_results = []
        endpoint = "api/useraction/vulnerabilities"
        if self.params_dict:
            endpoint += "?" + urlencode(self.params_dict, doseq=True)
        url = urljoin(self.server_prefix, endpoint)
        self.logger.info(f"getting vulnerabilities results from {url} ...")
        for results_list in self.results_generator(url):
            all_results.extend(results_list)
        self.logger.info(f"got {len(all_results)} vulnerabilities results...")
        return all_results
