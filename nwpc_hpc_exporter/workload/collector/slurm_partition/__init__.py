# coding=utf-8
from nwpc_hpc_exporter.workload.collector import BaseCollector

from .request import get_result


class Collector(BaseCollector):
    def __init__(self, collector_config):
        BaseCollector.__init__(self, collector_config)

    def request(self, category_list, client):
        return get_result(category_list, client)
