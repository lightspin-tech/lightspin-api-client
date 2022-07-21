from elasticsearch.exceptions import RequestError
from retry import retry
from elasticsearch import Elasticsearch, helpers, TransportError
from datetime import datetime

from lightspin_api_client.logger import Logger
from lightspin_api_client.config import Config
from lightspin_api_client.siem.siem_api import SiemApi

page_size = 200
config = Config()


class ElasticHandler:
    def __init__(self):
        self.logger = Logger("elastic_handler").logger
        self.logger.info("initializing elastic handler...")
        self.siem_results = None
        self.es_conn = None

    def update_siem_results_index(self):
        self.logger.info("adding elastic index to SIEM results")
        month = datetime.now().strftime("%m")
        year = datetime.now().strftime("%y")
        for item in self.siem_results:
            item["_index"] = f"{config.index_name_prefix}_{month}{year}"

    @retry(exceptions=(Exception,), delay=1, backoff=2, max_delay=4, tries=3)
    def create_es_conn(self):
        self.logger.info("creating elastic connection...")
        try:
            if config.elastic_user and config.elastic_password:
                return Elasticsearch(
                    hosts=config.elastic_hosts,
                    http_auth=(config.elastic_user, config.elastic_password),
                )
            else:
                print("missing elastic credentials, trying without it...")
                return Elasticsearch(hosts=config.elastic_hosts)
        except Exception as e:
            self.logger.error("failed to create elastic connection")
            self.logger.exception(e)
            raise e

    @retry(
        exceptions=(Exception, TransportError), delay=1, backoff=2, max_delay=4, tries=3
    )
    def elastic_transmit(self):
        self.logger.info(
            f"transmitting {len(self.siem_results)} siem results to elastic..."
        )
        try:
            month = datetime.now().strftime("%m")
            year = datetime.now().strftime("%y")
            self.es_conn.indices.create(
                index=f"{config.index_name_prefix}_{month}{year}", ignore=400
            )
            helpers.bulk(
                client=self.es_conn,
                actions=self.siem_results,
                chunk_size=config.elastic_transmit_chunk_size,
                request_timeout=config.elastic_transmit_request_timeout,
            )
        except RequestError as req_err:
            self.logger.error(f"Request error: {req_err}")
        except TransportError as conn_err:
            self.logger.error(f"Connection error: {conn_err}")
            self.es_conn = self.create_es_conn()
        except Exception as err:
            self.logger.error(f"Generic error: {err}")

    def run(self):
        self.logger.info("handler is started...")
        siem_api = SiemApi(
            {config.lightspin_url},
            config.lightspin_username,
            config.lightspin_password,
            config.lightspin_params_dict,
        )
        self.siem_results = siem_api.get_siem_results()
        if self.siem_results:
            self.update_siem_results_index()
            self.es_conn = self.create_es_conn()
            self.elastic_transmit()


if __name__ == "__main__":
    es_handler = ElasticHandler()
    es_handler.run()
