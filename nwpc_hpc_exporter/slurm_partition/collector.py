# coding=utf-8
import json
from paramiko import SSHClient

from nwpc_hpc_model.workload import QueryCategory, record_parser, value_saver
from nwpc_hpc_model.workload.slurm import SlurmQueryCategoryList, SlurmQueryModel
from nwpc_hpc_exporter.base.run import run_command


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


def run_sinfo_command(client: SSHClient) -> (str, str):
    command = 'sinfo -o "%20P %.5a %.20F %.30C"'
    return run_command(client, command)


def get_result(client, category_list) -> SlurmQueryModel or None:
    std_out_string, std_error_out_string = run_sinfo_command(client)
    result_lines = std_out_string.split("\n")

    category_list = build_category_list(category_list)

    model = SlurmQueryModel.build_from_table_category_list(result_lines, category_list)
    if model is None:
        return None
    return model
