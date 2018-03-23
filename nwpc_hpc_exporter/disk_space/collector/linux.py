import re
import locale
from nwpc_hpc_exporter.disk_space.collector import get_ssh_client, run_command


item_list = [
    'gb_blocks',
    'used_space',
    'available_space',
    'space_used_percent',
]


def run_df_command(client) -> (str,str):
    command = 'df -m'
    return run_command(client, command)


def get_disk_space(client) -> dict:
    std_out_string, std_error_out_string = run_df_command(client)
    result_lines = std_out_string.split("\n")

    detail_pattern = r'^(\S+) +(\S+) +(\S+) +(\S+) +(\S+) +(\S+)'
    detail_prog = re.compile(detail_pattern)
    disk_space_result = dict()
    file_system_list = list()

    for a_line in result_lines[1:]:
        detail_re_result = detail_prog.match(a_line)
        if detail_re_result:
            file_system = detail_re_result.group(1)

            mb_blocks = detail_re_result.group(2)
            if mb_blocks.isdigit():
                mb_blocks = locale.atoi(mb_blocks)

            used_space = detail_re_result.group(3)
            if used_space.isdigit():
                used_space = locale.atoi(used_space)

            space_used_percent = detail_re_result.group(4)
            if space_used_percent[-1] == '%':
                space_used_percent = space_used_percent[:-1]

            available_space = detail_re_result.group(5)
            if available_space.isdigit():
                available_space = locale.atoi(available_space)

            mounted_on = detail_re_result.group(6)

            current_file_system = {
                'file_system': file_system,
                'gb_blocks': mb_blocks / 1000.0,
                'used_space': used_space,
                'available_space': available_space,
                'space_used_percent': space_used_percent,
                'mounted_on': mounted_on
            }

            file_system_list.append(current_file_system)

    disk_space_result['file_systems'] = file_system_list
    return disk_space_result
