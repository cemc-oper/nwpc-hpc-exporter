import time

import click
import yaml
from prometheus_client import start_http_server, Gauge

from nwpc_hpc_exporter.disk_space.collector import get_disk_space

item_list = [
    'gb_blocks',
    'free_space',
    'space_used_percent',
    'inode_used',
    'inode_used_percent'
]


counter_dict = {
    an_item: Gauge(
        'hpc_disk_space_'+an_item, an_item, ['file_system']
    ) for an_item in item_list
}


def load_config(config_file):
    config = None
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def process_request(config):
    auth = config['global']['auth']
    t = 5
    disk_space_result = get_disk_space(auth)

    for a_file_system in disk_space_result['file_systems']:
        for an_item in item_list:
            if a_file_system[an_item] == "-":
                continue
            counter_dict[an_item].labels(
                file_system=a_file_system['file_system']
            ).set(a_file_system[an_item])

    time.sleep(t)


@click.command()
@click.option('--config-file', help="config file path")
def main(config_file):
    config = load_config(config_file)

    start_http_server(config['global']['exporter']['port'])

    while True:
        process_request(config)


if __name__ == '__main__':
    main()
