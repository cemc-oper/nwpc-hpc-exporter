import json
import yaml

from nwpc_hpc_exporter.disk_space.collector.linux import get_disk_space
from nwpc_hpc_exporter.disk_space.collector import get_ssh_client


def main():
    with open("./dist/conf/pi/test_disk_space.config.yml", 'r') as config_file:
        config = yaml.load(config_file)
    auth = config['global']['auth']
    print('getting ssh client...')
    client = get_ssh_client(auth)
    disk_space_result = get_disk_space(client)
    print(json.dumps(disk_space_result, indent=2))


if __name__ == "__main__":
    main()
