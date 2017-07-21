import time
import datetime
import socket

import click
import yaml
from prometheus_client import start_http_server, Gauge
import paramiko

from nwpc_hpc_exporter.disk_usage.collector import get_disk_usage, get_ssh_client

item_map = {
    'block_limits': [
        'current',
        'quota',
        'limit'
    ]
}


def load_config(config_file):
    config = None
    with open(config_file, 'r') as f:
        config = yaml.load(f)
    return config


def process_request(tasks):
    t = 5
    for a_task in tasks:
        auth = a_task['auth']
        client = a_task['client']

        try:
            disk_space_result = get_disk_usage(auth, client)
            for a_file_system in disk_space_result['file_systems']:
                block_limits = a_file_system['block_limits']
                for an_item in item_map['block_limits']:
                    a_task['block_limits_gauge_map'][an_item].labels(
                        file_system=a_file_system['file_system']
                    ).set(block_limits[an_item])
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


@click.command()
@click.option('--config-file', help="config file path")
def main(config_file):
    config = load_config(config_file)

    start_http_server(config['global']['exporter']['port'])

    tasks_config = config['tasks']
    print('getting ssh client...')
    tasks = []
    for a_task in tasks_config:
        block_limits_gauge_map = {
            an_item: Gauge(
                'hpc_' + a_task['name'] + '_disk_usage_block_limit_' + an_item, an_item, ['file_system']
            ) for an_item in item_map['block_limits']
        }
        client = get_ssh_client(a_task['auth'])
        tasks.append({
            'name': a_task['name'],
            'auth': a_task['auth'],
            'client': client,
            'block_limits_gauge_map': block_limits_gauge_map
        })

    print('exporter is working...')
    while True:
        process_request(tasks)


if __name__ == '__main__':
    main()
