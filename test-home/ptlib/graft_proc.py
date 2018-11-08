#!/usr/bin/env python3

import os

cmd_grep_graft = 'ps aux | grep -v grep | grep graft'
cmd_grep_graftnoded = 'ps aux | grep -v grep | grep graftnoded'
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


def mk_grep_exp_for_proc(proc):
    return 'ps aux | grep -v grep | grep ' + proc.name

def mk_kill_exp_for_proc(proc):
    return 'pkill -f ' + proc.name


class ProcPropsBase(object):
    def __init__(self, name):
        self.__name = name
        self.__host = None
        self.prepare_to_start()

    @property
    def name(self):
        return self.__name

    @property
    def host(self):
        return self.__host

    @host.setter
    def host(self, val):
        self.__host = val

    @property
    def cmd_grep(self):
        return mk_grep_exp_for_proc(self)

    @property
    def cmd_kill(self):
        return mk_kill_exp_for_proc(self)

    @property
    def cmd_start(self):
        sys.exit('ProcPropsBase::cmd_start - NOT IMPLEMENTED')

    def is_up(self, ssh_client):
        test = ssh_client.exec_ssh_cmd(self.cmd_grep)
        hit = self.name in test
        print('is-up: cmd-grep: [{}:{}] - [{}]: {}'.format(self.host.name, self.name, self.cmd_grep, hit))
        return hit

    def do_prestart_action(self, ssh_client):
        pass

    def prepare_to_start(self):
        pass

class ProcPropsGraftnoded(ProcPropsBase):
    def __init__(self):
        super().__init__('graftnoded')
        self.__path = ''
        self.__time_stamp = ''
        self.__host_list = None
        self.__cmd_start_cache = None

    @property
    def cmd_start(self):
        return self.__cmd_start_cache

    def pass_args_for_cmd_start(self, path, time_stamp, host_list):
        self.__path = path
        self.__time_stamp = time_stamp
        self.__host_list = host_list

    def do_prestart_action(self, ssh_client):
        print('do-prestart-action for {}, {}'.format(id(self), self.__prestart_action_complete))
        if not self.__prestart_action_complete:
            self.__prestart_action_complete = True
            test_suite_conf_file_name = os.path.join(self.__path, 'graft.conf.{}'.format(self.__time_stamp))
            self.__cmd_start_cache = mk_shell_cmd_to_start_graftnoded_with_config(self.host, test_suite_conf_file_name)
            conf_file = mk_config_file(self.host, self.__host_list)
            ssh_client.scp_put_from_str(test_suite_conf_file_name, conf_file)

    def prepare_to_start(self):
        self.__prestart_action_complete = False

    @property
    def cmd_mining_start(self):
        test_suite_conf_file_name = os.path.join(self.__path, 'graft.conf.{}'.format(self.__time_stamp))
        return mk_shell_cmd_to_start_mining_with_config(self.host, test_suite_conf_file_name)


class ProcPropsWalletCLI(ProcPropsBase):
    def __init__(self):
        super().__init__('graft-wallet-cli')

    @property
    def cmd_start(self):
        sys.exit('ProcPropsWalletCLI::cmd_start - NOT IMPLEMENTED')


class ProcPropsGraftServer(ProcPropsBase):
    def __init__(self):
        super().__init__('graft_server')
        self.__cmd_start_cache = None

    @property
    def cmd_start(self):
        return self.__cmd_start_cache

    def do_prestart_action(self, ssh_client):
        self.__cmd_start_cache = mk_shell_cmd_to_start_graft_server(self.host)


class GraftProc(object):
    def __init__(self):
        self.__gpnoded = ProcPropsGraftnoded()
        self.__gpwallet_cli = ProcPropsWalletCLI()
        self.__gp_server = ProcPropsGraftServer()

    @property
    def noded(self):
        return self.__gpnoded

    @property
    def wallet_cli(self):
        return self.__gpwallet_cli

    @property
    def server(self):
        return self.__gp_server

    @property
    def all(self):
        return [self.wallet_cli, self.server, self.noded]


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
    cmd = full_file_name + ' --testnet --detach --config-file ' + cfg_file_name
    return cmd

def mk_shell_cmd_to_start_mining_with_config(host, cfg_file_name):
    full_file_name = '/home/{}/projects/graft/bin/graftnoded'.format(host.user)
    cmd = full_file_name + ' --testnet --config-file ' + cfg_file_name + ' start_mining ' + host.wallet
    cmd += ' do_background_mining'
    return cmd

def mk_shell_cmd_to_start_graftnoded(host, host_list = []):
    full_file_name = '/home/{}/projects/graft/bin/graftnoded'.format(host.user)
    cmd_params = '--testnet --log-level 1 --testnet-rpc-bind-port {} --rpc-bind-ip {} --confirm-external-bind --detach'.format(host.port_nrpc, ip_any_local)
    cmd = '{} {}'.format(full_file_name, cmd_params)
    if host_list:
        cmd += ' ' + mk_shell_param_exclusive_node_list(host, host_list)
    return cmd

def mk_shell_cmd_to_start_graft_server(host):
    full_file_name = '/home/{}/projects/graft/bin/graft_server'.format(host.user)
    cmd_to_run_in_bkgnd = 'nohup ' + full_file_name + ' &'
    return cmd_to_run_in_bkgnd

#def there_is_running_graft(graft_grep_result, graft_launch_cmd):
#    if graft_grep_result:
#        print('grep-res: `{}`\ncmd `{}`'.format(graft_grep_result, graft_launch_cmd))
#    return graft_launch_cmd in graft_grep_result


#def mk_host_up(host):
#    cmd = mk_shell_cmd_for_start_graftnoded(host)
#    print('\n  ##  mk_host_up `{}`'.format(cmd))
#    exec_ssh_cmd(cmd, host)
#
#def mk_host_down(host):
#    kill_host_max_attempt_cnt = 10
#    cmd = cmd_kill_graft
#    while host_is_up(host):
#        #print('\n  ##  host `{}` is {}'.format(host.name, ('UP' if is_up else 'Down')))
#        print('\n  ##  host `{}` is UP'.format(host))
#        exec_ssh_cmd(cmd, host)
#        if host_is_up(host):
#            time.sleep(2)

