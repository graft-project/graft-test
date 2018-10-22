#!/usr/bin/env python3

import subprocess
from .ssh_ctl import SSHClient
import os
import shutil
import threading

#os.rename("path/to/current/file.foo", "path/to/new/destination/for/file.foo")
#shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

class HostLogCollector(object):
    def __init__(self, remote_ctl_script, func_mk_remote_path_to_log_dir):
        self.__remote_ctl_script = remote_ctl_script
        self.__func_mk_remote_path_to_log_dir = func_mk_remote_path_to_log_dir
        pass

    def name(self):
        return 'HostLogCollector'

    def prepare_log_capture(self, host_list):
        threads = self.do_work_in_parallel(host_list, self.thread_prepare_log_capture)
        for t in threads:
            t.join()

    def capture_log(self, host_list, dst_path):
        #print('capture_log, host-cnt:{}'.format(len(host_list)))
        threads = self.do_work_in_parallel(host_list, self.thread_capture_log, dst_path)
        for t in threads:
            t.join()

    def thread_prepare_log_capture(self, host, _):
        remote_log_path = self.__func_mk_remote_path_to_log_dir(host)
        self.put_and_mk_executable(host, self.__remote_ctl_script, remote_log_path)
        with SSHClient(host) as sc:
            remote_ctl_script = os.path.join(remote_log_path, os.path.basename(self.__remote_ctl_script))
            cmd_rnm_old_log = '{} --rnm-old-log {}'.format(remote_ctl_script, remote_log_path)
            #print('cmd-rnm-old-log: [{}]'.format(cmd_rnm_old_log))
            sc.exec_ssh_cmd(cmd_rnm_old_log)

    def thread_capture_log(self, host, dst_path):
        #print('thread_capture_log')

        remote_log_path = self.__func_mk_remote_path_to_log_dir(host)
        with SSHClient(host) as sc:
            remote_ctl_script = os.path.join(remote_log_path, os.path.basename(self.__remote_ctl_script))
            cmd_bkp_log = '{} --bkp-log {} {}'.format(remote_ctl_script, remote_log_path, host.name)
            #print('cmd-bkp-log: ,{}]'.format(cmd_bkp_log))
            sc.exec_ssh_cmd(cmd_bkp_log)

            remote_target_file = os.path.join(remote_log_path, '{}.txz'.format(host.name))
            #print('scp get for [{}]'.format(remote_target_file))
            sc.scp_get(remote_target_file, dst_path)

    def do_work_in_parallel(self, host_list, thread_func, path = ''):
        #print('do-work-in-parallel for [{}], host-cnt: {}'.format(thread_func.__name__, len(host_list)))
        threads = []
        for host in host_list:
            th = threading.Thread(target = thread_func, args = [host, path])
            th.start()
            threads.append(th)
        return threads

    def put(self, host):
        src_file = '/home/cybo/a/dev/lab/py/src/pt/ptlib/pt-remote-ctl'
        remote_path = '/home/ubuntu/.graft/testnet'
        with SSHClient(host) as sc:
            sc.scp_put(src_file, remote_path)
            cmd = 'chmod +x {}'.format(src_file)
            sc.exec_ssh_cmd(cmd)

    #src_file = '/home/cybo/a/dev/lab/py/src/pt/ptlib/pt-remote-ctl'
    #remote_path = '/home/ubuntu/.graft/testnet'

    def put_and_mk_executable(self, host, local_file, dst_remote_path):
        target_file = os.path.join(dst_remote_path, os.path.basename(local_file))
        cmd_mk_executable = 'chmod +x {}'.format(target_file)
        #print('host {}, cmd: {}'.format(host.name, cmd_mk_executable))

        with SSHClient(host) as sc:
            sc.scp_put(local_file, dst_remote_path)
            sc.exec_ssh_cmd(cmd_mk_executable)

            #cmd_ret = sc.exec_ssh_cmd('pwd')
            #print('pwd: [{}]'.format(cmd_ret))

    def get(self, host, remote_target_file, local_dst_path):
        #remote_target_file = '/home/ubuntu/.graft/testnet/121.txz'
        #local_dst_path = '/home/cybo/a/dev/lab/py/src'
        with SSHClient(host) as sc:
            sc.scp_get(remote_target_file, local_dst_path)

    def unpack(self, host):
        arc_file =  '/home/cybo/a/dev/lab/py/src/121.txz'
        cmd = 'tar xf {}'.format(arc_file)
        proc = subprocess.Popen(cmd.split(), stdout = subprocess.PIPE)
        output, error = proc.communicate()
        if output or error:
            print('out: {}\nerr: {}'.format(output, error))




