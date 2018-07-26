# coding=utf-8
from paramiko import SSHClient

from nwpc_hpc_model.workload.loadleveler import QueryCategory, QueryCategoryList, LoadLevelerQueryModel
from nwpc_hpc_model.workload.loadleveler import record_parser
from nwpc_hpc_model.workload.loadleveler import value_saver
from nwpc_hpc_exporter.base.run import run_command


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


def run_llclass_command(client: SSHClient) -> (str, str):
    command = "/usr/bin/llclass -l"
    return run_command(client, command)


def get_result(category_list, client: SSHClient) -> dict or None:
    std_out_string, std_error_out_string = run_llclass_command(client)
    result_lines = std_out_string.split("\n")

    category_list = build_category_list(category_list)

    model = LoadLevelerQueryModel.build_from_category_list(result_lines, category_list)
    return model
