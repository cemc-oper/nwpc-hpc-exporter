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
