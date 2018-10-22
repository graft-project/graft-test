#!/usr/bin/env python3

import os
import time
import datetime

def mk_dirs(path):
    os.makedirs(path, exist_ok = True)

def curr_test_name():
    test_name = os.environ.get('PYTEST_CURRENT_TEST')
    spc_idx = test_name.rfind(' ')
    if spc_idx > 0:
        test_name = test_name[:spc_idx]
    test_name = test_name.replace('test_', '').replace('_', '-').replace('/', '-').replace('.py::', '-')
    return test_name

class ReportController(object):
    report_home_dir = 'test-run-report'
    host_log_dir_name = 'logs'
    request_dir_name = 'requests'

    def __init__(self, curr_work_dir, log_collector, host_list):
        self.__host_list = host_list
        self.__log_collector = log_collector
        self.__cwd = curr_work_dir
        #print('report-contorller cwd [{}]'.format(self.__cwd))

        time_stamp_fmt = '%Y%m%d-%H%M%S-%f'
        time.sleep(0.002)
        now = datetime.datetime.today()
        self.__time_stamp = now.strftime(time_stamp_fmt)[:-3][2:]
        self.__report_timed_dir_name = os.path.join(self.__cwd, self.report_home_dir, self.__time_stamp)
        self.__current_report_name = ''

    def __del__(self):
            print('\n[{}] died ...'.format(self))

    @property
    def name(self):
        return 'report-contoller'

    @property
    def time_stamp(self):
        return self.__time_stamp

    @property
    def report_home_path(self):
        return self.__report_timed_dir_name

    @property
    def current_report_name(self):
        return self.__current_report_name

    @property
    def current_report_home_path(self):
        return os.path.join(self.report_home_path, self.__current_report_name)

    @property
    def current_report_log_path(self):
        return os.path.join(self.current_report_home_path, self.host_log_dir_name)

    @property
    def current_report_requests_path(self):
        return os.path.join(self.current_report_home_path, self.request_dir_name)

    def start_report(self):
        self.__current_report_name = curr_test_name()
        mk_dirs(self.current_report_log_path)
        mk_dirs(self.current_report_requests_path)
        #print('ReportController - start for [{}]'.format(self.current_report_name))
        self.__log_collector.prepare_log_capture(self.__host_list())
        #print('\nstart-report, host-cnt:{}'.format(len(self.__host_list())))

    def finalize_report(self):
        #print('ReportController - finalize for [{}]'.format(self.current_report_name))
        self.__log_collector.capture_log(self.__host_list(), self.current_report_log_path)


