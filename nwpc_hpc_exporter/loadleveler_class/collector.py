# coding=utf-8
import json
from paramiko import SSHClient, AutoAddPolicy

from nwpc_hpc_model.loadleveler import QueryCategory, QueryCategoryList, QueryModel, QueryProperty, QueryItem
from nwpc_hpc_model.loadleveler import record_parser
from nwpc_hpc_model.loadleveler import value_saver


def build_category_list(category_list_config):
    category_list = QueryCategoryList()
    for an_item in category_list_config:
        category = QueryCategory(
            category_id=an_item['id'],
            display_name=an_item['display_name'],
            label=an_item['display_name'],
            record_parser_class=getattr(record_parser, an_item['record_parser_class']),
            record_parser_arguments=tuple(an_item['record_parser_arguments']),
            value_saver_class=getattr(value_saver, an_item['value_saver_class']),
            value_saver_arguments=tuple(an_item['value_saver_arguments'])
        )
        category_list.append(category)
    return category_list


def run_command(auth) -> (str,str):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(auth['host'], auth['port'], auth['user'], auth['password'])

    command = "/usr/bin/llclass -l"

    stdin, stdout, stderr = client.exec_command(command)
    std_out_string = stdout.read().decode('UTF-8')
    std_error_out_string = stderr.read().decode('UTF-8')
    client.close()

    return std_out_string, std_error_out_string


def get_result(auth, category_list) -> dict:
    std_out_string, std_error_out_string = run_command(auth)
    result_lines = std_out_string.split("\n")

    category_list = build_category_list(category_list)

    model = QueryModel.build_from_category_list(result_lines, category_list)
    model_dict = model.to_dict()
    return model_dict


if __name__ == "__main__":
    auth = {
        'host': 'uranus.hpc.nmic.cn',
        'port': 22,
        'user': 'wangdp',
        'password': 'perilla'
    }
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
