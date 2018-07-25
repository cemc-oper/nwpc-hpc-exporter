# coding=utf-8
import json
import os
import yaml

from nwpc_hpc_exporter.workload.collector.loadleveler_class.request import get_result


def get_dist_directory():
    current_path = os.path.dirname(__file__)
    return os.path.join(current_path, "../../../dist")


def main():
    with open(os.path.join(get_dist_directory(), "conf/test.config.yml"), 'r') as config_file:
        config = yaml.load(config_file)
    auth = config['auth']
    category_list = [
        {
            "id": "name",
            "display_name": "Name",
            "label": "Name",
            "record_parser_class": "DetailLabelParser",
            "record_parser_arguments": ["Name"],
            "value_saver_class": "StringSaver",
            "value_saver_arguments": []
        },
        {
            "id": "free_slots",
            "display_name": "Free Slots",
            "label": "Free_slots",
            "record_parser_class": "DetailLabelParser",
            "record_parser_arguments": ["Free_slots"],
            "value_saver_class": "NumberSaver",
            "value_saver_arguments": []
        },
        {
            "id": "maximum_slots",
            "display_name": "Maximum Slots",
            "label": "Maximum_slots",
            "record_parser_class": "DetailLabelParser",
            "record_parser_arguments": ["Maximum_slots"],
            "value_saver_class": "NumberSaver",
            "value_saver_arguments": []
        },
    ]
    result = get_result(auth, category_list)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
