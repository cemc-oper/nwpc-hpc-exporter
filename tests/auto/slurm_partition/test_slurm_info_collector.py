# coding: utf-8
import yaml
from pathlib import Path
from nwpc_hpc_exporter.slurm_partition import collector


def load_config(config_file_path):
    config = None
    with open(config_file_path, 'r') as f:
        config = yaml.load(f)
    return config


def find_prop_by_id(item, prop_id):
    prop_item = None
    for a_prop in item.props:
        if a_prop.category.id == prop_id:
            prop_item = a_prop
            break
    return prop_item


def test_get_result(monkeypatch):
    def mock_run_command(command, ssh_client):
        result_file = Path(Path(__file__).parent, 'data/sinfo.query.txt')
        with open(result_file, 'r') as f:
            text = f.read()
            return text, ''

    monkeypatch.setattr(collector, "run_command", mock_run_command)

    client = object()

    config = load_config(Path(Path(__file__).parent, 'data/slurm_partition.config.yml'))
    category_list = config['category_list']

    result = collector.get_result(client, category_list)

    assert(len(result.items) == 4)

    serial_item = result.items[0]
    prop = find_prop_by_id(serial_item, "sinfo.partition")
    assert(prop.map['text'] == 'serial')
    prop = find_prop_by_id(serial_item, "sinfo.avail")
    assert(prop.map['text'] == 'up')
    prop = find_prop_by_id(serial_item, "sinfo.nodes")
    assert(prop.map['text'] == '0/0/20/20')
    prop = find_prop_by_id(serial_item, "sinfo.cpus")
    assert(prop.map['text'] == '0/0/640/640')

    normal_item = result.items[1]

    prop = find_prop_by_id(normal_item, "sinfo.partition")
    assert(prop.map['text'] == 'normal')
    prop = find_prop_by_id(normal_item, "sinfo.avail")
    assert(prop.map['text'] == 'up')
    prop = find_prop_by_id(normal_item, "sinfo.nodes")
    assert(prop.map['text'] == '224/1139/141/1504')
    prop = find_prop_by_id(normal_item, "sinfo.cpus")
    assert(prop.map['text'] == '6784/36832/4512/48128')
