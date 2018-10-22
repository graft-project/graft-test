#!/usr/bin/env python3

import os
import ptlib.driver as drv
from ptlib.host_log_collector import HostLogCollector
from ptlib.host_requester import HostRequester
from ptlib.report_ctl import ReportController

class TestRunEnvironment(object):
    def __init__(self):
        self.__hosts = []

    @property
    def hosts(self):
        return self.__hosts

    @hosts.setter
    def hosts(self, val):
        self.__hosts = val

def mk_remote_path_to_log_dir(host):
    return '/home/{}/.graft/testnet/'.format(host.user)
    #return '/home/{}/projects/graft/bin/graftnoded'.format(host.user)

class TestSession(object):
    def __init__(self, tests_root_path):
        self.__ptlib_path = os.path.join(tests_root_path, 'ptlib')
        print('TestSession: ptlib-path [{}]'.format(self.__ptlib_path))
        self.__env = TestRunEnvironment()
        remote_ctl_script_file = os.path.join(self.__ptlib_path, 'pt-remote-ctl')
        self.__hlc = HostLogCollector(remote_ctl_script_file, mk_remote_path_to_log_dir)
        self.__report_ctl = ReportController(os.getcwd(), self.__hlc, lambda: self.__env.hosts)
        self.__hrq = HostRequester(lambda: self.__env.hosts, lambda: self.__report_ctl.current_report_requests_path, drv)

    @property
    def core(self):
        return drv

    @property
    def env(self):
        return self.__env

    @property
    def host_requester(self):
        return self.__hrq

    @property
    def host_log_collector(self):
        return self.__hlc

    @property
    def report_ctl(self):
        return self.__report_ctl


