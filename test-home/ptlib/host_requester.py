#!/usr/bin/env python3

import os
import threading
import json
import logging
import requests
import datetime

log = logging.getLogger(__name__)

class HostRequester(object):
    def __init__(self, host_list, dst_path, core):
        self.__host_list = host_list
        self.__dst_path = dst_path
        self.__core = core

    def mk_new_response_set(self):
        hosts = self.__host_list()
        resps = {}
        for h in hosts:
            resps[h.name] = { "host_name": h.name, "host_ip": h.ip, "host_wallet": h.wallet, "resp": {} }
        return resps

    def mk_file_name(self, func_name):
        time_stamp_fmt = '%H%M%S-%f'
        now = datetime.datetime.today()
        ts = now.strftime(time_stamp_fmt)[:-3]
        return '{}-{}.json'.format(ts, func_name)

    def do_requests_in_parallel(self, thread_func):
        threads = []
        hosts = self.__host_list()
        resps = self.mk_new_response_set()
        for host in hosts:
            th = threading.Thread(target = thread_func, args = [host, resps[host.name]])
            th.start()
            threads.append(th)
        return threads, resps

    def dump_to_file(self, func_name, text_to_dump):
        fn = os.path.join(self.__dst_path(), self.mk_file_name(func_name))
        with open(fn, 'w') as outfile:
            outfile.write(text_to_dump)

    def name(self):
        return 'HostRequester'

    def get_connections(self):
        pass

    def get_peer_list(self):
        pass

    def thread_get_tunnels(self, host, resp):
        url_nrpc = self.__core.mk_node_rpc_rta_url_by_host(host)
        #log.info('Node RPC url: {}'.format(url_nrpc))

        json_req = {"jsonrpc":"2.0","id":"0","method":"get_tunnels"}
        #log.info('JSON to send: {}'.format(json.dumps(json_req)))

        hdrs = {'Content-Type':'application/json'}
        r = requests.post(url_nrpc, json = json_req, headers = hdrs)
        rs = r.text
        #print(' # resp: {}'.format(rs))
        resp['resp'] = json.loads(rs)

    def get_tunnels(self):
        threads, resps = self.do_requests_in_parallel(self.thread_get_tunnels)
        for t in threads:
            t.join()
        self.dump_to_file('get-tunnels', json.dumps(resps, indent = 2))

