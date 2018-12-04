#!/usr/bin/env python3

import os
import threading
import json
import logging
import requests
import datetime

log = logging.getLogger(__name__)

def mk_file_name(func_name):
    time_stamp_fmt = '%H%M%S-%f'
    now = datetime.datetime.today()
    ts = now.strftime(time_stamp_fmt)[:-3]
    return '{}-{}.json'.format(ts, func_name)

def write_hint(outfile, hint):
    if hint:
        hint = '\nhint: ' + hint + '\n'
        outfile.write(hint)


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

    def mk_get_supernode_list_request(self, host, only_good_ones):
        port = self.__core.port_srpc
        return 'http://{}:{}/debug/supernode_list/{}'.format(host.ip, port, ('0' if only_good_ones else '1'))
        #url = 'http://' + host.ip + ':' + str(port) + '/debug/supernode_list/1'

    def do_requests_in_parallel(self, thread_func):
        threads = []
        hosts = self.__host_list()
        resps = self.mk_new_response_set()
        for host in hosts:
            th = threading.Thread(target = thread_func, args = [host, resps[host.name]])
            th.start()
            threads.append(th)
        return threads, resps

    def dump_to_file(self, func_name, text_to_dump, hint):
        fn = os.path.join(self.__dst_path(), mk_file_name(func_name))
        with open(fn, 'w') as outfile:
            write_hint(outfile, hint)
            outfile.write(text_to_dump)

    def name(self):
        return 'HostRequester'


    def thread_get_connections(self, host, resp):
        url = self.__core.mk_node_rpc_url(host.ip, self.__core.port_nrpc)
        log.info('Node RPC url: {}'.format(url))

        json_req = {"jsonrpc":"2.0","id":"0","method":"get_connections"}
        log.info('JSON to send: {}'.format(json.dumps(json_req)))

        r = requests.post(url, json = json_req, headers = self.__core.default_rpc_req_headers())
        resp['resp'] = json.loads(r.text)

    def get_connections(self, hint = '', wait_before = 0):
        self.__core.wait(wait_before)
        threads, resps = self.do_requests_in_parallel(self.thread_get_connections)
        for t in threads:
            t.join()
        self.dump_to_file('get-connections', json.dumps(resps, indent = 2), hint)

        #def send_get_connections(ip_addr, port, snode_ip = ip_any_local, snode_port = port_srpc):
        #    url_nrpc = mk_node_rpc_url(ip_addr, port)
        #    log.info('Node RPC url: {}'.format(url_nrpc))

        #    json_req = {"jsonrpc":"2.0","id":"0","method":"get_connections"}
        #    log.info('JSON to send: {}'.format(json.dumps(json_req)))

        #    r = requests.post(url_nrpc, json = json_req, headers = default_rpc_req_headers())
        #    rs = r.content
        #    rs = r.text
        #    print(' # resp: {}'.format(rs))
        #    dump_to_file('get-conns', ip_addr, rs)
        #    #print(r.json())
        #    #print(' # resp: {}'.format(json.dumps(r.json(), indent = 2, ensure_ascii = False, encoding = 'utf8')))

    def thread_get_peer_list(self, host, resp):
        url = 'http://{}:{}/get_peer_list'.format(host.ip, self.__core.port_nrpc)
        log.info('Node RPC url: {}'.format(url))
        r = requests.get(url, headers = self.__core.default_rpc_req_headers())
        resp['resp'] = json.loads(r.text)

    def get_peer_list(self, hint = '', wait_before = 0):
        self.__core.wait(wait_before)
        threads, resps = self.do_requests_in_parallel(self.thread_get_peer_list)
        for t in threads:
            t.join()
        self.dump_to_file('get-peer-list', json.dumps(resps, indent = 2), hint)

      #def send_get_peer_list(ip_addr, port):
      #    url_nrpc = 'http://' + ip_addr + ':' + str(port) + '/get_peer_list'
      #    log.info('Node RPC url: {}'.format(url_nrpc))

      #    hdrs = {'Content-Type':'application/json'}
      #    r = requests.get(url_nrpc, headers = hdrs)
      #    rs = json.dumps(r.json(), indent = 2)
      #    print(' # resp: {}'.format(rs))
      #    dump_to_file('get-peer-list', ip_addr, rs)



    def thread_get_supernode_good(self, host, resp):
        url = self.mk_get_supernode_list_request(host, True)
        log.info('Snode RPC url: {}'.format(url))
        r = requests.get(url, headers = self.__core.default_rpc_req_headers())
        resp['resp'] = json.loads(r.text)

    def get_supernode_good_list(self, hint = '', wait_before = 0):
        self.__core.wait(wait_before)
        threads, resps = self.do_requests_in_parallel(self.thread_get_supernode_good)
        for t in threads:
            t.join()
        self.dump_to_file('get-supernode-list-good', json.dumps(resps, indent = 2), hint)


    def thread_get_supernode_all(self, host, resp):
        url = self.mk_get_supernode_list_request(host, False)
        log.info('Snode RPC url: {}'.format(url))
        r = requests.get(url, headers = self.__core.default_rpc_req_headers())
        resp['resp'] = json.loads(r.text)

    def get_supernode_all_list(self, hint = '', wait_before = 0):
        self.__core.wait(wait_before)
        threads, resps = self.do_requests_in_parallel(self.thread_get_supernode_all)
        for t in threads:
            t.join()
        self.dump_to_file('get-supernode-list-all', json.dumps(resps, indent = 2), hint)


    def thread_get_tunnels(self, host, resp):
        url_nrpc = self.__core.mk_node_rpc_rta_url_by_host(host)
        log.info('Node RPC url: {}'.format(url_nrpc))

        json_req = {"jsonrpc":"2.0","id":"0","method":"get_tunnels"}
        log.info('JSON to send: {}'.format(json.dumps(json_req)))

        r = requests.post(url_nrpc, json = json_req, headers = self.__core.default_rpc_req_headers())
        rs = r.text
        #print(' # resp: {}'.format(rs))
        resp['resp'] = json.loads(rs)

    def get_tunnels(self, hint = '', wait_before = 0):
        self.__core.wait(wait_before)
        threads, resps = self.do_requests_in_parallel(self.thread_get_tunnels)
        for t in threads:
            t.join()
        self.dump_to_file('get-tunnels', json.dumps(resps, indent = 2), hint)


