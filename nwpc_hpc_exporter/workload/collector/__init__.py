# coding=utf-8
import datetime
import time
import socket

import paramiko
from prometheus_client import Gauge

from nwpc_hpc_exporter.base.connection import get_ssh_client


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

    def process_single_task(self, task):
        pass

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
