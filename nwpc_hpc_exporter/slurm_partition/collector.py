# coding=utf-8
import json
from paramiko import SSHClient, AutoAddPolicy

from nwpc_hpc_model.workload import QueryCategory, record_parser, value_saver
from nwpc_hpc_model.workload.slurm import SlurmQueryCategoryList, SlurmQueryModel


def build_category_list(category_list_config):
    category_list = SlurmQueryCategoryList()
    for an_item in category_list_config:
        category = QueryCategory(
            category_id=an_item['id'],
            display_name=an_item['display_name'],
            label=an_item['label'],
            record_parser_class=getattr(record_parser, an_item['record_parser_class']),
            record_parser_arguments=tuple(an_item['record_parser_arguments']),
            value_saver_class=getattr(value_saver, an_item['value_saver_class']),
            value_saver_arguments=tuple(an_item['value_saver_arguments'])
        )
        category_list.append(category)
    return category_list


def get_ssh_client(auth):
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(auth['host'], auth['port'], auth['user'], auth['password'])
    return client


def run_command(client) -> (str, str):
    command = 'sinfo -o "%20P %.5a %.20F %.30C"'

    stdin, stdout, stderr = client.exec_command(command)
    std_out_string = stdout.read().decode('UTF-8')
    std_error_out_string = stderr.read().decode('UTF-8')

    return std_out_string, std_error_out_string


def get_result(client, category_list) -> SlurmQueryModel or None:
    std_out_string, std_error_out_string = run_command(client)
    result_lines = std_out_string.split("\n")

    category_list = build_category_list(category_list)

    model = SlurmQueryModel.build_from_table_category_list(result_lines, category_list)
    if model is None:
        return None
    return model
