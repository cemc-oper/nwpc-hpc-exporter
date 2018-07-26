# coding=utf-8
import datetime
import time
import socket

import paramiko
from prometheus_client import Gauge

from nwpc_hpc_model.base.query_item import get_property_data
from nwpc_hpc_exporter.base.connection import get_ssh_client


class TokenValueExtractor(object):
    def __init__(self, sep, index):
        self.sep = sep
        self.index = index

    def extract(self, value):
        tokens = value.split(self.sep)
        return tokens[self.index]


class BaseCollector(object):
    def __init__(self, collector_config):
        self.collector_config = collector_config
        self.gauge_list = []
        self.gauge_label_config = []

    def setup(self):
        self.gauge_list = self.generate_gauge_list(self.collector_config)
        self.gauge_label_config = self.collector_config['metric']['gauge_label']

    def process_request(self, tasks):
        t = 5
        for a_task in tasks:
            auth = a_task['auth']

            try:
                self.process_single_task(a_task)
            except paramiko.ssh_exception.SSHException as ssh_exception:
                print(datetime.datetime.now(), "reconnect ssh")
                a_task['client'] = get_ssh_client(auth)
            except socket.gaierror as socket_exception:
                print(datetime.datetime.now(), "get socket gaierror exception.")
                print(datetime.datetime.now(), "wait 5 seconds...")
                time.sleep(5)
                print(datetime.datetime.now(), "reconnect ssh")
                a_task['client'] = get_ssh_client(auth)

        time.sleep(t)

    def request(self, category_list, client):
        return None

    def process_single_task(self, task):
        client = task['client']
        category_list = task['category_list']

        model = self.request(category_list, client)
        if model is None:
            return
        for an_item in model.items:
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

    @classmethod
    def generate_gauge_list(cls, collector_config):
        metric_config = collector_config['metric']
        gauge_label_config = metric_config['gauge_label']

        gauge_label_names = []
        for a_gauge_label_config in gauge_label_config:
            label_name = a_gauge_label_config['name']
            gauge_label_names.append(label_name)

        gauge_list_config = metric_config['gauge_list']

        gauge_list = []
        for a_gauge_config in gauge_list_config:
            a_gauge = {}
            a_gauge.update(a_gauge_config)
            a_gauge['metric'] = Gauge(a_gauge_config['name'], a_gauge_config['name'], gauge_label_names)
            gauge_list.append(a_gauge)
        return gauge_list
