# coding=utf-8
import time

import click
import yaml
from prometheus_client import start_http_server, Gauge

from nwpc_hpc_exporter.loadleveler_class.collector import get_result

item = [
    'free_slots',
    'maximum_slots'
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
    result = get_result(task['auth'], task['category_list'])
    for a_class in result['items']:
        class_prop_item = find_prop_by_id(a_class, task['identify_category_id'])

        for an_item in task['metrics_item']:
            prop_item = find_prop_by_id(a_class, an_item)

            task['gauge_map'][an_item].labels(
                class_name=class_prop_item['value']
            ).set(prop_item['value'])

    time.sleep(t)


@click.command()
@click.option('--config-file', help="config file path")
def main(config_file):
    config = load_config(config_file)

    start_http_server(8000)

    category_list = config['category_list']
    gauge_map = {
        an_item: Gauge(
            'hpc_loadleveler_class_' + an_item, an_item, ['class_name']
        ) for an_item in config['metrics_item']
    }
    task = {
        'gauge_map': gauge_map,
        'category_list': category_list,
        'auth': config['global']['auth'],
        'metrics_item': config['metrics_item'],
        'identify_category_id': config['identify_category_id']
    }

    while True:
        process_request(task)


if __name__ == '__main__':
    main()
