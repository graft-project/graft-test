#!/usr/bin/env python3

from ssh_ctl import SSHClient
#from graft_proc import GraftProc
import os
import time
import threading
import copy
#from typing import NamedTuple


def try_proc_to_shutdown(ssh_client, proc):
    kill_host_max_attempt_cnt = 10
    while proc.is_up(ssh_client):
        print('  ##  proc `{}:{}` is UP'.format(proc.host.name, proc.name))
        ssh_client.exec_ssh_cmd(proc.cmd_kill)
        print('  ##  proc `{}:{}` exec {}'.format(proc.host.name, proc.name, proc.cmd_kill))
        time.sleep(1)
        if proc.is_up(ssh_client):
            time.sleep(2)
        else:
            print('  ##  proc `{}:{}` is down'.format(proc.host.name, proc.name))
            break

class HostCtl(object):
    def __init__(self, host_list):
        self.__host_list = host_list

    def do_action_in_parallel(self, thread_func, proc, **kwargs):
        threads = []
        hosts = self.__host_list()
        for h in hosts:
            p = copy.deepcopy(proc)
            p.host = h
            th = threading.Thread(target = thread_func, args = [p], kwargs = kwargs)
            th.start()
            threads.append(th)
        return threads

    def thread_start_all2(self, proc, **kwargs):
        proc.prepare_to_start()
        with SSHClient(proc.host) as sc:
            try_proc_to_shutdown(sc, proc)
            proc.do_prestart_action(sc)
            print('  ## starting proc {}:{}: [{}]'.format(proc.host.name, proc.name, proc.cmd_start))
            sc.exec_ssh_cmd(proc.cmd_start)

    def start_all2(self, proc_list):
        for proc in proc_list:
            threads = self.do_action_in_parallel(self.thread_start_all2, proc)
            for t in threads:
                t.join()


        #, test_time_stamp, remote_path_to_log
        #kwargs = { 'test_time_stamp': test_time_stamp, 'remote_path_to_log': remote_path_to_log }
        #threads = self.do_action_in_parallel(self.thread_start_all2, **kwargs)

    def thread_stop_all(self, proc, **kwargs):
        with SSHClient(proc.host) as sc:
            try_proc_to_shutdown(sc, proc)

    def stop_all(self, proc_list):
        for proc in proc_list:
            threads = self.do_action_in_parallel(self.thread_stop_all, proc)
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
            try_proc_to_shutdown(sc, proc)
            sc.scp_put_from_str(test_suite_conf_file_name, conf_file)
            print('  ## starting host {}: [{}]'.format(host.name, cmd))
            sc.exec_ssh_cmd(cmd)


#    def start_all(self):
#        hosts = self.__host_list()
#        for h in hosts:
#            cmd = mk_shell_cmd_to_start_graftnoded(h, hosts)
#            with SSHClient(h) as sc:
#                try_proc_to_shutdown(sc, h)
#                print('  ## starting host {}: [{}]'.format(h.name, cmd))
#                sc.exec_ssh_cmd(cmd)



        #hosts = self.__host_list()
        #for h in hosts:
        #    cmd = mk_shell_cmd_to_start_graftnoded(h, hosts)
        #    with SSHClient(h) as sc:
        #        try_proc_to_shutdown(sc, h)
        #        print('  ## starting host {}: [{}]'.format(h.name, cmd))
        #        sc.exec_ssh_cmd(cmd)

        #with SSHClient(host) as sc:
        #    try_proc_to_shutdown(sc, host)


