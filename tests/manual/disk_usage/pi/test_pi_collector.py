import json
import os
import yaml

from nwpc_hpc_exporter.disk_usage.collector.pi.request import get_disk_usage
from nwpc_hpc_exporter.base.connection import get_ssh_client


def get_dist_directory():
    current_path = os.path.dirname(__file__)
    return os.path.join(current_path, "../../../../dist")


def main():
    with open(os.path.join(get_dist_directory(), "test/disk_usage/pi/test.config.yml"), 'r') as config_file:
        config = yaml.load(config_file)
    auth = config['auth']
    client = get_ssh_client(auth)
    category_list = config['category_list']
    model = get_disk_usage(category_list, client)
    print(json.dumps(model.to_dict(), indent=2))


if __name__ == "__main__":
    main()
