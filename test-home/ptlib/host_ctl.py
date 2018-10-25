#!/usr/bin/env python3

from .ssh_ctl import SSHClient
import time

cmd_grep_graft = 'ps aux | grep -v grep | grep graft'
cmd_kill_graft = 'pkill graft'
ip_any_local = '0.0.0.0'

def mk_shell_param_exclusive_node_list(host, host_list):
    param_name = '--add-exclusive-node '
    nl = ''
    for h in host_list:
        if h.name == host.name:
            continue
        if nl:
            nl += ' '
        nl += param_name + h.ip
    return nl

def mk_shell_cmd_to_start_graftnoded(host, host_list = []):
    full_file_name = '/home/{}/projects/graft/bin/graftnoded'.format(host.user)
    cmd_params = '--testnet --log-level 1 --testnet-rpc-bind-port {} --rpc-bind-ip {} --confirm-external-bind --detach'.format(host.port_nrpc, ip_any_local)
    cmd = '{} {}'.format(full_file_name, cmd_params)
    if host_list:
        cmd += ' ' + mk_shell_param_exclusive_node_list(host, host_list)
    return cmd

#def there_is_running_graft(graft_grep_result, graft_launch_cmd):
#    if graft_grep_result:
#        print('grep-res: `{}`\ncmd `{}`'.format(graft_grep_result, graft_launch_cmd))
#    return graft_launch_cmd in graft_grep_result


def mk_host_up(host):
    cmd = mk_shell_cmd_for_start_graftnoded(host)
    print('\n  ##  mk_host_up `{}`'.format(cmd))
    exec_ssh_cmd(cmd, host)

def mk_host_down(host):
    kill_host_max_attempt_cnt = 10
    cmd = cmd_kill_graft
    while host_is_up(host):
        #print('\n  ##  host `{}` is {}'.format(host.name, ('UP' if is_up else 'Down')))
        print('\n  ##  host `{}` is UP'.format(host))
        exec_ssh_cmd(cmd, host)
        if host_is_up(host):
            time.sleep(2)

def host_is_up(ssh_client):
    graft_grep = ssh_client.exec_ssh_cmd(cmd_grep_graft)
    is_up = 'graftnoded' in graft_grep
    return is_up

def try_host_to_shutdown(ssh_client, host):
    kill_host_max_attempt_cnt = 10
    cmd = cmd_kill_graft
    while host_is_up(ssh_client):
        print('  ##  host `{}` is UP'.format(host.name))
        ssh_client.exec_ssh_cmd(cmd_kill_graft)
        time.sleep(1)
        if host_is_up(ssh_client):
            time.sleep(2)
        else:
            print('  ##  host `{}` is down'.format(host.name))
            break

        #print('\n  ##  host `{}` is {}'.format(host.name, ('UP' if is_up else 'Down')))

class HostCtl(object):
    def __init__(self, host_list):
        self.__host_list = host_list

    def start_all(self):
        hosts = self.__host_list()
        for h in hosts:
            cmd = mk_shell_cmd_to_start_graftnoded(h, hosts)
            with SSHClient(h) as sc:
                try_host_to_shutdown(sc, h)
                sc.exec_ssh_cmd(cmd)




