#!/usr/bin/env python3

import os
import pwd
import select
import paramiko
import logging
from scp import SCPClient
import time
import datetime

logging.getLogger("paramiko").setLevel(logging.WARNING)

def get_username():
    return pwd.getpwuid(os.getuid())[0]

def ssh_pvt_key_file_name():
    return '/home/{}/.ssh/id_rsa'.format(get_username())

class SSHClient(object):
    def __init__(self, host):
        rsa_key_file = ssh_pvt_key_file_name()
        k = paramiko.RSAKey.from_private_key_file(rsa_key_file)
        self.__ssh_client = paramiko.SSHClient()
        self.__ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.__ssh_client.connect(hostname = host.name, username = host.user, pkey = k)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.__ssh_client.close()

    def exec_ssh_cmd(self, cmd):
        sc_stdin, sc_stdout, sc_stderr = self.__ssh_client.exec_command(cmd)
        ssh_cmd_out = ''
        while not sc_stdout.channel.exit_status_ready():
            # Only print data if there is data to read in the channel
            if sc_stdout.channel.recv_ready():
                rl, wl, xl = select.select([ sc_stdout.channel ], [ ], [ ], 0.0)
                if len(rl) > 0:
                    tmp = sc_stdout.channel.recv(1024)
                    #output = tmp.decode()
                    #print(output)
                    ssh_cmd_out += tmp.decode()
        return ssh_cmd_out

    def scp_put(self, files, remote_path):
    	with SCPClient(self.__ssh_client.get_transport()) as scp:
            scp.put(files, remote_path)

    def scp_get(self, remote_target_file, local_dst_path):
    	with SCPClient(self.__ssh_client.get_transport()) as scp:
            scp.get(remote_target_file, local_dst_path)

#def exec_ssh_cmd(cmd, host):
#    rsa_key_file = ssh_pvt_key_file_name()
#    k = paramiko.RSAKey.from_private_key_file(rsa_key_file)
#    sc = paramiko.SSHClient()
#    sc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    sc.connect(hostname = host.name, username = host.user, pkey = k)
#    #sc.connect(srv, username = usr, password=password)
#    sc_stdin, sc_stdout, sc_stderr = sc.exec_command(cmd)
#
#    ssh_cmd_out = ''
#    while not sc_stdout.channel.exit_status_ready():
#        # Only print data if there is data to read in the channel
#        if sc_stdout.channel.recv_ready():
#            rl, wl, xl = select.select([ sc_stdout.channel ], [ ], [ ], 0.0)
#            if len(rl) > 0:
#                tmp = sc_stdout.channel.recv(1024)
#                #output = tmp.decode()
#                #print(output)
#                ssh_cmd_out += tmp.decode()
#    sc.close()
#    #print('\n  ## ssh-cmd-out: {}'.format(ssh_cmd_out))
#    return ssh_cmd_out


