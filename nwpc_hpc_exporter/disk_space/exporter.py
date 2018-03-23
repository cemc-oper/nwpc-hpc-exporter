# coding=utf-8

import time
import datetime
import socket

import click
import yaml
import paramiko
from prometheus_client import start_http_server, Gauge

from nwpc_hpc_exporter.disk_space import collector


def load_config(config_file):
    config = None
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def generate_process_request_function(config):
    collector_config = config['collector']
    collector_type = collector_config['type']

    collector_module = getattr(collector, collector_type)

    counter_dict = {
        an_item: Gauge(
            'hpc_disk_space_' + an_item, an_item, ['file_system']
        ) for an_item in collector_module.item_list
    }

    def process_request(client):
        t = 5
        disk_space_result = collector_module.get_disk_space(client)

        for a_file_system in disk_space_result['file_systems']:
            for an_item in collector_module.item_list:
                if a_file_system[an_item] == "-":
                    continue
                counter_dict[an_item].labels(
                    file_system=a_file_system['file_system']
                ).set(a_file_system[an_item])

        time.sleep(t)

    return process_request


@click.command()
@click.option('--config-file', help="config file path")
def main(config_file):
    config = load_config(config_file)
    process_request = generate_process_request_function(config)

    start_http_server(config['global']['exporter']['port'], addr='0.0.0.0')

    auth = config['global']['auth']
    print('getting ssh client...')
    client = collector.get_ssh_client(auth)

    print('exporter is working...')
    while True:
        try:
            process_request(client)
        except paramiko.ssh_exception.SSHException as ssh_exception:
            print(datetime.datetime.now(), "reconnect ssh")
            client = collector.get_ssh_client(auth)
        except socket.gaierror as socket_exception:
            print(datetime.datetime.now(), "get socket gaierror exception.")
            print(datetime.datetime.now(), "wait 5 seconds...")
            time.sleep(5)
            print(datetime.datetime.now(), "reconnect ssh")
            client = collector.get_ssh_client(auth)


if __name__ == '__main__':
    main()
