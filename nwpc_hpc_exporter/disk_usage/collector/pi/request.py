# coding: utf-8
from paramiko import SSHClient
from nwpc_hpc_exporter.base.run import run_command
from nwpc_hpc_model.disk_usage.pi import PiDiskUsageCategoryList, PiDiskUsageQueryModel


def run_disk_usage_command(client: SSHClient) -> (str, str):
    command = 'quotainfo'
    return run_command(client, command)


def get_disk_usage(category_list: dict, client: SSHClient) -> PiDiskUsageQueryModel:
    std_out_string, std_error_out_string = run_disk_usage_command(client)
    result_lines = std_out_string.split("\n")

    category_list = PiDiskUsageCategoryList.build_from_config(category_list)
    model = PiDiskUsageQueryModel.build_from_category_list(result_lines, category_list)

    return model
