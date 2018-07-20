# coding: utf-8
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

    def setup(self):
        self.gauge_list = self.generate_gauge_list(self.collector_config)

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
        gauge_list_config = metric_config['gauge_list']

        gauge_list = []
        for a_gauge_config in gauge_list_config:
            gauge_list.append({
                'metric': Gauge(a_gauge_config['name'], a_gauge_config['name'], gauge_label_config),
                'name': a_gauge_config['name'],
                'category_id': a_gauge_config['category_id']
            })
        return gauge_list
