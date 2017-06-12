import json
import os
import yaml

from nwpc_hpc_exporter.disk_space.collector import get_disk_space


def get_dist_directory():
    current_path = os.path.dirname(__file__)
    return os.path.join(current_path, "../../../dist")


def main():
    with open(os.path.join(get_dist_directory(), "conf/test.config.yml"), 'r') as config_file:
        config = yaml.load(config_file)
    auth = config['auth']
    disk_space_result = get_disk_space(auth)
    print(json.dumps(disk_space_result, indent=2))


if __name__ == "__main__":
    main()
