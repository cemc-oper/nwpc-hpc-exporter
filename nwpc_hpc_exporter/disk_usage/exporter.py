# coding: utf-8
import importlib

import click
import yaml
from prometheus_client import start_http_server

from nwpc_hpc_exporter.base.connection import get_ssh_client


def load_config(config_file):
    config = None
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def get_collector(config):
    collector_config = config['collector']
    collector_type = collector_config['type']

    collector_module = importlib.import_module("nwpc_hpc_exporter.disk_usage.collector." + collector_type)
    collector_class = collector_module.Collector

    return collector_class


def get_gauge_map_method(config):
    collector_config = config['collector']
    collector_type = collector_config['type']

    collector_module = importlib.import_module("nwpc_hpc_exporter.disk_usage.collector." + collector_type)
    gauge_map_method = collector_module.generate_task_gauge_map

    return gauge_map_method


@click.command()
@click.option('--config-file', help="config file path")
def main(config_file):
    config = load_config(config_file)

    start_http_server(config['global']['exporter']['port'])

    collector_class = get_collector(config)
    collector = collector_class(config['collector'])
    collector.setup()

    category_list = config['collector']['category_list']
    tasks_config = config['tasks']
    print('getting ssh client...')
    tasks = []
    for a_task in tasks_config:
        client = get_ssh_client(a_task['auth'])

        tasks.append({
            'owner': a_task['owner'],
            'repo': a_task['repo'],
            'auth': a_task['auth'],
            'category_list': category_list,
            'client': client,
        })

    print('exporter is working...')
    while True:
        collector.process_request(tasks)


if __name__ == '__main__':
    main()
