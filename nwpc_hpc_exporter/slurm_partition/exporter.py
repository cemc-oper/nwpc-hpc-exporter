# coding=utf-8
import time
import datetime
import socket

import click
import yaml
from prometheus_client import start_http_server, Gauge
import paramiko

from nwpc_hpc_exporter.slurm_partition.collector import get_result, get_ssh_client


def get_token_from_index(index, text, sep='/'):
    tokens = text.split(sep)
    return tokens[index]


def create_index_value_extractor(index):
    def value_extractor(prop):
        text = prop['text']
        value = get_token_from_index(index, text)
        return value
    return value_extractor


items = [
    {
        'metrics_name': 'nodes_available',
        'prop_id': 'sinfo.nodes',
        'value_extractor': create_index_value_extractor(0)
    },
    {
        'metrics_name': 'nodes_idle',
        'prop_id': 'sinfo.nodes',
        'value_extractor': create_index_value_extractor(1)
    },
    {
        'metrics_name': 'nodes_other',
        'prop_id': 'sinfo.nodes',
        'value_extractor': create_index_value_extractor(2)
    },
    {
        'metrics_name': 'nodes_total',
        'prop_id': 'sinfo.nodes',
        'value_extractor': create_index_value_extractor(3)
    },
    {
        'metrics_name': 'cpus_available',
        'prop_id': 'sinfo.cpus',
        'value_extractor': create_index_value_extractor(0)
    },
    {
        'metrics_name': 'cpus_idle',
        'prop_id': 'sinfo.cpus',
        'value_extractor': create_index_value_extractor(1)
    },
    {
        'metrics_name': 'cpus_other',
        'prop_id': 'sinfo.cpus',
        'value_extractor': create_index_value_extractor(2)
    },
    {
        'metrics_name': 'cpus_total',
        'prop_id': 'sinfo.cpus',
        'value_extractor': create_index_value_extractor(3)
    }
]


def load_config(config_file):
    config = None
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def find_prop_by_id(item, prop_id):
    prop_item = None
    for a_prop in item['props']:
        if a_prop['id'] == prop_id:
            prop_item = a_prop
            break
    return prop_item


def process_request(task):
    t = 5
    result = get_result(task['client'], task['category_list'])
    if result is None:
        time.sleep(t)
        return
    for a_partition in result['items']:
        partition_prop_item = find_prop_by_id(a_partition, task['identify_category_id'])

        for an_item in task['metrics_items']:
            prop_item = find_prop_by_id(a_partition, an_item['prop_id'])
            value = an_item['value_extractor'](prop_item)

            task['gauge_map'][an_item['metrics_name']].labels(
                partition_name=partition_prop_item['value']
            ).set(value)

    time.sleep(t)


@click.command()
@click.option('--config-file', help="config file path")
def main(config_file):
    config = load_config(config_file)

    start_http_server(config['global']['exporter']['port'])

    category_list = config['category_list']
    gauge_map = {
        an_item['metrics_name']: Gauge(
            'hpc_slurm_sinfo_' + an_item['metrics_name'], an_item['metrics_name'], ['partition_name']
        ) for an_item in items
    }

    print('getting ssh client...')
    client = get_ssh_client(config['global']['auth'])

    task = {
        'gauge_map': gauge_map,
        'category_list': category_list,
        'auth': config['global']['auth'],
        'client': client,
        'metrics_items': items,
        'identify_category_id': config['identify_category_id']
    }

    print('exporter is working...')
    while True:
        try:
            process_request(task)
        except paramiko.ssh_exception.SSHException as ssh_exception:
            print(datetime.datetime.now(), "reconnect ssh")
            task['client'] = get_ssh_client(config['global']['auth'])
        except socket.gaierror as socket_exception:
            print(datetime.datetime.now(), "get socket gaierror exception.")
            print(datetime.datetime.now(), "wait 5 seconds...")
            time.sleep(5)
            print(datetime.datetime.now(), "reconnect ssh")
            task['client'] = get_ssh_client(config['global']['auth'])


if __name__ == '__main__':
    main()
