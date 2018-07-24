# coding: utf-8

from nwpc_hpc_model.base.query_item import get_property_data
from nwpc_hpc_exporter.disk_space.collector import BaseCollector

from .request import get_disk_space


class Collector(BaseCollector):
    def __init__(self, collector_config):
        BaseCollector.__init__(self, collector_config)

    def process_single_task(self, task):
        client = task['client']
        category_list = task['category_list']

        disk_space_result_model = get_disk_space(category_list, client)
        for an_item in disk_space_result_model.items:
            for a_gauge in self.gauge_list:
                labels = {}
                for a_label_config in self.gauge_label_config:
                    label_name = a_label_config['name']
                    label_type = a_label_config['type']
                    if label_type == "task":
                        config_key = a_label_config['config_key']
                        labels[label_name] = task[config_key]
                    elif label_type == "category":
                        category_id = a_label_config['category_id']
                        labels[label_name] = get_property_data(an_item, category_id)
                    else:
                        raise Exception("label type not supported:", label_type)

                a_gauge['metric'].labels(**labels).set(
                    get_property_data(an_item, a_gauge['category_id']))
