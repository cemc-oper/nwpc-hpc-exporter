# coding=utf-8

from nwpc_hpc_model.base.query_item import get_property_data
from nwpc_hpc_exporter.workload.collector import BaseCollector

from .request import get_result


class TokenValueExtractor(object):
    def __init__(self, sep, index):
        self.sep = sep
        self.index = index

    def extract(self, value):
        tokens = value.split(self.sep)
        return tokens[self.index]


class Collector(BaseCollector):
    def __init__(self, collector_config):
        BaseCollector.__init__(self, collector_config)

    def process_single_task(self, task):
        client = task['client']
        category_list = task['category_list']

        disk_space_result_model = get_result(category_list, client)
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

                data = get_property_data(an_item, a_gauge['category_id'])

                if 'value_extractor' in a_gauge:
                    value_extractor_config = a_gauge['value_extractor']
                    value_extractor_class = globals()[value_extractor_config['class']]
                    value_extractor_arguments = value_extractor_config['arguments']

                    value_extractor = value_extractor_class(**value_extractor_arguments)
                    value = value_extractor.extract(data)
                else:
                    value = data

                a_gauge['metric'].labels(**labels).set(value)
