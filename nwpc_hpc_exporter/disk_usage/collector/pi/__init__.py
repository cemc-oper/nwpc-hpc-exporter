# coding=utf-8

from nwpc_hpc_model.base.query_item import get_property_data
from nwpc_hpc_exporter.disk_usage.collector import BaseCollector

from .request import get_disk_usage


class Collector(BaseCollector):
    def __init__(self, collector_config):
        BaseCollector.__init__(self, collector_config)

    def process_single_task(self, task):
        client = task['client']
        category_list = task['category_list']

        disk_usage_result_model = get_disk_usage(category_list, client)
        for an_item in disk_usage_result_model.items:
            for a_gauge in self.gauge_list:
                a_gauge['metric'].labels(
                    owner=task['owner'],
                    repo=task['repo'],
                    file_system=get_property_data(an_item, "disk_usage.dir")
                ).set(get_property_data(an_item, a_gauge['category_id']))
