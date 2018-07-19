# coding=utf-8
import re
import locale

from paramiko import SSHClient
from nwpc_hpc_exporter.base.run import run_command
from nwpc_hpc_model.disk_usage.aix import AixDiskUsageCategoryList, AixDiskUsageQueryModel, QueryCategory, \
    record_parser, value_saver
from nwpc_hpc_model.base.query_item import get_property_data


disk_usage_command_map = {
    'aix': '/cma/u/app/sys_bin/cmquota ${USER}',
    'pi': 'quotainfo'
}


def run_disk_usage_command(task_type: str, client: SSHClient) -> (str, str):
    command = disk_usage_command_map[task_type]
    return run_command(client, command)


def get_disk_usage(task_type: str, auth: dict, category_list: dict, client: SSHClient) -> dict:
    std_out_string, std_error_out_string = run_disk_usage_command(task_type, client)
    result_lines = std_out_string.split("\n")

    category_list = AixDiskUsageCategoryList.build_from_config(category_list)
    model = AixDiskUsageQueryModel.build_from_category_list(result_lines, category_list)

    quota_result = dict()
    file_system_list = list()

    for an_item in model.items:
        current_file_system = dict()
        current_file_system['file_system'] = get_property_data(an_item, "disk_usage.file_system")
        current_file_system['type'] = get_property_data(an_item, "disk_usage.quota_type")
        block_limits = {
            'current': get_property_data(an_item, "disk_usage.block_limits.current"),
            'quota': get_property_data(an_item, "disk_usage.block_limits.quota"),
            'limit': get_property_data(an_item, "disk_usage.block_limits.limit"),
            'in_doubt': get_property_data(an_item, "disk_usage.block_limits.in_doubt"),
            'grace': get_property_data(an_item, "disk_usage.block_limits.grace")
        }
        file_limits = {
            'files': get_property_data(an_item, "disk_usage.file_limits.files"),
            'quota': get_property_data(an_item, "disk_usage.file_limits.quota"),
            'limit': get_property_data(an_item, "disk_usage.file_limits.limit"),
            'in_doubt': get_property_data(an_item, "disk_usage.file_limits.in_doubt"),
            'grace': get_property_data(an_item, "disk_usage.file_limits.grace"),
            'remarks': get_property_data(an_item, "disk_usage.file_limits.remarks")
        }
        current_file_system['block_limits'] = block_limits
        current_file_system['file_limits'] = file_limits
        file_system_list.append(current_file_system)

    quota_result['file_systems'] = file_system_list
    quota_result['user'] = auth['user']
    return quota_result
