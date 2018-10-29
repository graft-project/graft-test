#!/usr/bin/env python3

from ssh_ctl import SSHClient
import os
import time
import threading

cmd_grep_graft = 'ps aux | grep -v grep | grep graft'
cmd_kill_graft = 'pkill graft'
ip_any_local = '0.0.0.0'

#  Ports
#    8081 - block explorer port
#  286 00 - load balancer http port
#  286 43 - load balancer https port
#  286 80 - p2p node port
#  286 81 - rpc node port
#  286 90 - rpc supernode port

#testnet = 1
#net-id = 14686520-4172-7420-6f76-205761722035
#log-level = 4
#testnet-rpc-bind-port = 28681
#rpc-bind-ip = 0.0.0.0
#confirm-external-bind = 1
#
#seed-node = 54.226.23.229:28680
#seed-node = 54.197.32.149:28680
#seed-node = 52.90.236.226:28680
#
#add-exclusive-node = 54.226.23.229:28680
#add-exclusive-node = 54.197.32.149:28680
#add-exclusive-node = 52.90.236.226:28680

def cfg_file_add_switch(cfg, switch_name):
    cfg += switch_name + ' = 1' + '\n'
    return cfg

def cfg_file_add_test_net(cfg):
    return cfg_file_add_switch(cfg, 'testnet')

def cfg_file_add_detach(cfg):
    return cfg_file_add_switch(cfg, 'detach')

def cfg_file_add_net_id(cfg, net_id):
    cfg += 'net-id = ' + net_id + '\n'
    return cfg

def cfg_file_add_log_level(cfg, ll_val):
    cfg += 'log-level = ' + str(ll_val) + '\n'
    return cfg

def cfg_file_add_testnet_rpc_bind_port(cfg, port):
    cfg += 'testnet-rpc-bind-port = ' + str(port) + '\n'
    return cfg

def cfg_file_add_testnet_rpc_bind_ip(cfg, ip_addr):
    cfg += 'rpc-bind-ip = ' + ip_addr + '\n'
    return cfg_file_add_switch(cfg, 'confirm-external-bind')

def add_node_list(cfg, param_name, node_list, ip_with_port, but_node = None):
    if node_list:
        for n in node_list:
            if but_node and n.ip == but_node.ip:
                continue
            cfg += '\n' + param_name + ' = ' + n.ip
            if ip_with_port:
                cfg += ':' + str(n.port_nrpc)
        cfg += '\n'
    return cfg

def cfg_file_add_seed_nodes(cfg, host_list):
    return add_node_list(cfg, 'seed-node', host_list, True)

def cfg_file_add_exclusive_nodes(cfg, host_list, this_node):
    return add_node_list(cfg, 'add-exclusive-node', host_list, False, this_node)

def mk_shell_param_exclusive_node_list(host):
    available_hosts = [ host1, host2, host3 ]
    param_name = '--add-exclusive-node '
    nl = ''
    for h in available_hosts:
        if h.name == host.name:
            continue
        if nl:
            nl += ' '
        nl += param_name + h.ip
    return nl
    return cfg

#testnet-rpc-bind-port = 28681
def mk_config_file(this_node = None, host_list = []):
    cfg = ''
    #cfg = cfg_file_add_test_net(cfg)
    #cfg = cfg_file_add_detach(cfg)
    cfg = cfg_file_add_net_id(cfg, '14686520-4172-7420-6f76-205761722035')
    cfg = cfg_file_add_log_level(cfg, 1)
    cfg = cfg_file_add_testnet_rpc_bind_port(cfg, 28681)
    cfg = cfg_file_add_testnet_rpc_bind_ip(cfg, ip_any_local)
    cfg = cfg_file_add_seed_nodes(cfg, host_list)
    cfg = cfg_file_add_exclusive_nodes(cfg, host_list, this_node)
    return cfg

#testnet-rpc-bind-port = 28681
#rpc-bind-ip = 0.0.0.0
#confirm-external-bind = 1
#
#seed-node = 54.226.23.229:28680
#seed-node = 54.197.32.149:28680
#seed-node = 52.90.236.226:28680
#
#add-exclusive-node = 54.226.23.229:28680

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

def mk_shell_cmd_to_start_graftnoded_with_config(host, cfg_file_name):
    full_file_name = '/home/{}/projects/graft/bin/graftnoded'.format(host.user)
    return full_file_name + ' --testnet --detach --config-file ' + cfg_file_name

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
    #print('try_host_to_shutdown for {}'.format(host.name))
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
                print('  ## starting host {}: [{}]'.format(h.name, cmd))
                sc.exec_ssh_cmd(cmd)

    def do_action_in_parallel(self, thread_func, **kwargs):
        threads = []
        hosts = self.__host_list()
        for h in hosts:
            th = threading.Thread(target = thread_func, args = [h], kwargs = kwargs)
            th.start()
            threads.append(th)
        return threads

    def thread_start_all2(self, host, **kwargs):
        test_time_stamp = kwargs['test_time_stamp']
        remote_path_to_log = kwargs['remote_path_to_log']
        #print('{}\n{}\n{}'.format(host.name, test_time_stamp, remote_path_to_log))
        test_suite_conf_file_name = os.path.join(remote_path_to_log, 'graft.conf.{}'.format(test_time_stamp))
        conf_file = mk_config_file(host, self.__host_list())
        #print(conf_file)
        cmd = mk_shell_cmd_to_start_graftnoded_with_config(host, test_suite_conf_file_name)
        with SSHClient(host) as sc:
            try_host_to_shutdown(sc, host)
            sc.scp_put_from_str(test_suite_conf_file_name, conf_file)
            print('  ## starting host {}: [{}]'.format(host.name, cmd))
            sc.exec_ssh_cmd(cmd)

    def start_all2(self, test_time_stamp, remote_path_to_log):
        kwargs = { 'test_time_stamp': test_time_stamp, 'remote_path_to_log': remote_path_to_log }
        threads = self.do_action_in_parallel(self.thread_start_all2, **kwargs)
        for t in threads:
            t.join()

    def thread_stop_all(self, host, **kwargs):
        with SSHClient(host) as sc:
            try_host_to_shutdown(sc, host)

    def stop_all(self):
        threads = self.do_action_in_parallel(self.thread_stop_all)
        for t in threads:
            t.join()

    def start(self, host_idx, test_time_stamp, remote_path_to_log):
        host = self.__host_list()[host_idx]
        test_suite_conf_file_name = os.path.join(remote_path_to_log, 'graft.conf.{}'.format(test_time_stamp))
        print('HostCtl::start for host idx:{} - {}\ntest-suite-conf-file: [{}]'.format(host_idx, host.name, test_suite_conf_file_name))
        conf_file = mk_config_file(host, self.__host_list())
        print(conf_file)
        cmd = mk_shell_cmd_to_start_graftnoded_with_config(host, test_suite_conf_file_name)
        with SSHClient(host) as sc:
            try_host_to_shutdown(sc, host)
            sc.scp_put_from_str(test_suite_conf_file_name, conf_file)
            print('  ## starting host {}: [{}]'.format(host.name, cmd))
            sc.exec_ssh_cmd(cmd)


        #hosts = self.__host_list()
        #for h in hosts:
        #    cmd = mk_shell_cmd_to_start_graftnoded(h, hosts)
        #    with SSHClient(h) as sc:
        #        try_host_to_shutdown(sc, h)
        #        print('  ## starting host {}: [{}]'.format(h.name, cmd))
        #        sc.exec_ssh_cmd(cmd)

        #with SSHClient(host) as sc:
        #    try_host_to_shutdown(sc, host)


