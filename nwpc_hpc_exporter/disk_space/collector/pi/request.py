# coding: utf-8
from paramiko import SSHClient
from nwpc_hpc_exporter.base.run import run_command
from nwpc_hpc_model.disk_space.pi import PiDiskSpaceCategoryList, PiDiskSpaceQueryModel


def run_df_command(client) -> (str, str):
    command = 'df -m'
    return run_command(client, command)


def get_disk_space(category_list: dict, client: SSHClient) -> PiDiskSpaceQueryModel:
    std_out_string, std_error_out_string = run_df_command(client)
    result_lines = std_out_string.split("\n")

    category_list = PiDiskSpaceCategoryList.build_from_config(category_list)
    model = PiDiskSpaceQueryModel.build_from_category_list(result_lines, category_list)

    return model
