#!/usr/bin/env python3

import os
import ptlib.driver as drv
from ptlib.host_log_collector import HostLogCollector
from ptlib.host_requester import HostRequester
from ptlib.report_ctl import ReportController
from ptlib.host_ctl import HostCtl
from math import factorial, pow

class TestRunConfig(object):
    def __init__(self):
        self.__nodes = []
        self.__wait = {}

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, val):
        self.__nodes = val

    @property
    def wait(self):
        return self.__wait

    @wait.setter
    def wait(self, val):
        self.__wait = val

    def count_of_arrangement(self):
        n = len(self.nodes)
        m = 2
        cnt = factorial(n) / factorial(n - m)
        return int(cnt)

    def count_of_arrangement_with_self(self):
        n = len(self.nodes)
        m = 2
        return int(pow(n, m))

def mk_remote_path_to_log_dir(host):
    return '/home/{}/.graft/testnet/'.format(host.user)
    #return '/home/{}/projects/graft/bin/graftnoded'.format(host.user)

class TestSession(object):
    def __init__(self, tests_root_path):
        self.__ptlib_path = os.path.join(tests_root_path, 'ptlib')
        print('TestSession: ptlib-path [{}]'.format(self.__ptlib_path))
        self.__cfg = TestRunConfig()
        remote_ctl_script_file = os.path.join(self.__ptlib_path, 'pt-remote-ctl')
        self.__hlc = HostLogCollector(remote_ctl_script_file, mk_remote_path_to_log_dir)
        self.__report_ctl = ReportController(os.getcwd(), self.__hlc, lambda: self.__cfg.nodes)
        self.__hrq = HostRequester(lambda: self.__cfg.nodes, lambda: self.__report_ctl.current_report_requests_path, drv)
        self.__host_ctl = HostCtl(lambda: self.__cfg.nodes)

    @property
    def core(self):
        return drv

    @property
    def cfg(self):
        return self.__cfg

    @property
    def host_requester(self):
        return self.__hrq

    @property
    def host_log_collector(self):
        return self.__hlc

    @property
    def host_ctl(self):
        return self.__host_ctl

    @property
    def report_ctl(self):
        return self.__report_ctl


