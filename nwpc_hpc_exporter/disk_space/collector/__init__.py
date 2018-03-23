# coding=utf-8
from paramiko import SSHClient, AutoAddPolicy


def get_ssh_client(auth: dict) -> SSHClient:
    client = SSHClient()
    client.set_missing_host_key_policy(AutoAddPolicy())
    client.connect(auth['host'], auth['port'], auth['user'], auth['password'])
    return client


def run_command(client: SSHClient, command: str) -> (str, str):
    stdin, stdout, stderr = client.exec_command(command)
    std_out_string = stdout.read().decode('UTF-8')
    std_error_out_string = stderr.read().decode('UTF-8')

    return std_out_string, std_error_out_string
