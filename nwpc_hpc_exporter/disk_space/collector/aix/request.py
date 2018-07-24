# coding: utf-8
from paramiko import SSHClient
from nwpc_hpc_exporter.base.run import run_command
from nwpc_hpc_model.disk_space.aix import AixDiskSpaceCategoryList, AixDiskSpaceQueryModel


def run_df_command(client) -> (str, str):
    command = '/usr/bin/df -g'
    return run_command(client, command)


def get_disk_space(category_list: dict, client: SSHClient) -> AixDiskSpaceQueryModel:
    std_out_string, std_error_out_string = run_df_command(client)
    result_lines = std_out_string.split("\n")

    category_list = AixDiskSpaceCategoryList.build_from_config(category_list)
    model = AixDiskSpaceQueryModel.build_from_category_list(result_lines, category_list)

    return model
