#!/usr/bin/env python3

import os, sys
sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)))

import argparse
import json
import logging
import requests
import shelve
import time
import datetime
import subprocess
from ssh_ctl import SSHClient
from request_template import RequestTemplate
from typing import NamedTuple

class Host(NamedTuple):
    name: str
    ip: str
    user: str
    wallet: str
    port_nrpc: int

def wait(wait_sec):
    if wait_sec:
        time.sleep(wait_sec)

def load_config(path, conf_file, conf_obj):
    conf = os.path.join(path, conf_file)

    if not os.path.exists(conf):
        sys.exit('File with environment description [{}] not found'.format(conf))

    if not os.path.isfile(conf):
        sys.exit('[{}] is not a file - cannot be read'.format(conf))

    with open(conf) as jf:
        js = jf.read()
        jo = json.loads(js)

        nodes = []
        for obj in jo['nodes']:
           nodes.append(Host(**obj))

        conf_obj.nodes = nodes
        conf_obj.wait = jo['wait']

    print('conf [{}] loaded, node-cnt:{}'.format(conf, len(nodes)))

def load_conf_by_current_conftest(curr_conftest, conf_obj):
    cfg_file = 'conf.json'
    curr_path = os.path.dirname(os.path.realpath(curr_conftest))
    return load_config(curr_path, cfg_file, conf_obj)

def mk_remote_path_to_log_dir(host):
    return '/home/{}/.graft/testnet/'.format(host.user)
    #return '/home/{}/projects/graft/bin/graftnoded'.format(host.user)

def mk_time_stamp_for_test():
    time_stamp_fmt = '%Y%m%d-%H%M%S-%f'
    now = datetime.datetime.today()
    time_stamp = now.strftime(time_stamp_fmt)[:-3][2:]
    return time_stamp

#########################################################################################

def drv_name():
    return 'main graft test driver'

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

#  Ports
#    8081 - block explorer port
#  286 00 - load balancer http port
#  286 43 - load balancer https port
#  286 80 - p2p node port
#  286 81 - rpc node port
#  286 90 - rpc supernode port

#class Car(NamedTuple):
#    color: str
#    mileage: float
#    automatic: bool


gn00 = 'gn00'
gn01 = 'gn01'
gn02 = 'gn02'
gn03 = 'gn03'

gn0X_user = 'ubuntu'

ip_n0 = "18.206.213.77"
ip_n1 = "54.226.23.229"
ip_n2 = "54.197.32.149"
ip_n3 = "52.90.236.226"

ip_n0_local = "172.31.31.68"
ip_n1_local = "172.31.18.232"
ip_n2_local = "172.31.29.186"
ip_n3_local = "172.31.31.22"

ip_any_local = '0.0.0.0'

port_nrpc = 28681
port_srpc = 28690
#port_wrpc = 29982
port_wrpc = 28982

port_srpc1 = 28691
port_srpc2 = 28692
port_srpc3 = 28693

wa0 = ""
wa1 = "F4KrqowwEoY6K9J8dV75toToyYYmHdMbkWgFCm4A9uMhND3uGtnMFU4gAGLBVYFEbz2zC9jrVvCS96x3HUcy6nAd4q4Robb"
wa2 = "F43mWaMKqTM5uhxG2kjyrRS9QBEGYS9PmbEUBYQjkEd51U9ThEeKvjDFYxr7pSkd5WLZKLj7Go1FsEP2uLY8RrCTPnnnJ7n"
wa3 = "F5ciEZFQzy7Ln4QDtqR4d415ih6gBHtb8CY8gPDF97iiKwRfGmLZ5yJMGYtKvDZaWDVng4pjpdN9eY9c3vkA8a44Km89Wfx"

host0 = Host(gn00, ip_n0, gn0X_user, wa0, port_nrpc)
host1 = Host(gn01, ip_n1, gn0X_user, wa1, port_nrpc)
host2 = Host(gn02, ip_n2, gn0X_user, wa2, port_nrpc)
host3 = Host(gn03, ip_n3, gn0X_user, wa3, port_nrpc)

cmd_grep_graft = 'ps aux | grep -v grep | grep graft'
cmd_kill_graft = 'pkill graft'

cmd_node_down = cmd_kill_graft
cmd_node_1_down = cmd_kill_graft
cmd_node_2_down = cmd_kill_graft
cmd_node_3_down = cmd_kill_graft

persist_storage_name = 'persistent-storage-uuid'
persist_key_timestamp = 'timestamp'

logging.basicConfig(format = '%(message)s', level = logging.INFO)
log = logging.getLogger(__name__)

cmd_grep_graft = 'ps aux | grep -v grep | grep graft'
cmd_kill_graft = 'pkill graft'

run_ctx = {'faked-timestamp': 0}

def log_url_json(url, jo):
    log.info('RPC url: {}'.format(url))
    log.info('JSON to send: {}'.format(json.dumps(jo)))

def mk_full_file_name_from_local_name(file_name):
    path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(path, file_name)

def get_test_name(test_file_name):
    test_name_pfx = 'test_'
    return test_file_name[len(test_name_pfx):] if test_file_name.startswith(test_name_pfx) else test_file_name

#def load_initial_timestamp_from_json():
#    json_file = os.path.join(os.path.realpath(__file__), announce_json_file)
#    with open(json_file) as jf:
#        js = jf.read()
#        jo = json.loads(js)
#        ts = jo['params']['timestamp']
#        log.info('New timestamp value loaded from json-file: {}'.format(ts))
#        return ts

def exec_ssh_cmd(cmd, host):
    with SSHClient(host) as sc:
        return sc.exec_ssh_cmd(cmd)

def get_next_timestamp():
    with shelve.open(persist_storage_name) as db:
        if not persist_key_timestamp in db:
            db[persist_key_timestamp] = load_initial_timestamp_from_json()

        ts = db[persist_key_timestamp]
        db[persist_key_timestamp] += 1
    return ts

def get_current_timestamp():
    return int(time.time())

def get_faked_timestamp():
    if not run_ctx['faked-timestamp']:
        run_ctx['faked-timestamp'] = get_current_timestamp()
    run_ctx['faked-timestamp'] += 1
    return run_ctx['faked-timestamp']

def get_hires_timestamp():
    return str(time.perf_counter()).replace('.','')

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

def mk_shell_cmd_for_start_graftnoded(host):
    full_file_name = '/home/{}/projects/graft/bin/graftnoded'.format(host.user)
    cmd_params = '--testnet --log-level 1 --testnet-rpc-bind-port {} --rpc-bind-ip {} --confirm-external-bind --detach'.format(port_nrpc, ip_any_local)
    return '{} {} {}'.format(full_file_name, cmd_params, mk_shell_param_exclusive_node_list(host))

def mk_node_rpc_url(ip_addr, port):
    return 'http://' + ip_addr + ':' + str(port) + '/json_rpc'

def mk_node_rpc_url_by_host(host):
    return mk_node_rpc_url(host.ip, port_nrpc)


def mk_wallet_rpc_url(ip_addr, port):
    return 'http://' + ip_addr + ':' + str(port) + '/json_rpc'

def mk_wallet_rpc_url_by_host(host):
    return mk_wallet_rpc_url(host.ip, port_wrpc)


def mk_node_rpc_rta_url(ip_addr, port):
    return 'http://' + ip_addr + ':' + str(port) + '/json_rpc/rta'

def mk_node_rpc_rta_url_by_host(host):
    return mk_node_rpc_rta_url(host.ip, port_nrpc)
    #return 'http://' + host.ip + ':' + str(port) + '/json_rpc/rta'


def mk_netw_addr(ip_addr, port):
    return ip_addr + ':' + str(port) + '/dapi/v2.0'
#"network_address":"54.226.23.229:28690/dapi/v2.0"

def mk_snode_rpc_dapi2_url(host, method):
    return 'http://' + host.ip + ':' + str(port_srpc) + '/dapi/v2.0/' + method


def mk_full_file_name_from_local_name(file_name):
    path = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(path, file_name)

def default_rpc_req_headers():
    return {'Content-Type':'application/json'}

def mk_sale_request(src, amount):
    jo = json.loads(json.dumps(RequestTemplate.sale))
    jo['params']['Address'] = src.wallet
    jo['params']['Amount'] = amount
    return mk_snode_rpc_dapi2_url(src, 'sale'), jo, default_rpc_req_headers()

def mk_sale_details_request(src, pay_id, block_num):
    jo = json.loads(json.dumps(RequestTemplate.sale_details))
    jo['params']['PaymentID'] = pay_id
    jo['params']['BlockNumber'] = block_num
    return mk_snode_rpc_dapi2_url(src, 'sale_details'), jo, default_rpc_req_headers()

def mk_pay_request(src, merchant_addr, pay_id, block_num, amount, tx):
    jo = json.loads(json.dumps(RequestTemplate.pay))
    jo['params']['Address'] = merchant_addr
    jo['params']['PaymentID'] = pay_id
    jo['params']['BlockNumber'] = block_num
    jo['params']['Amount'] = amount
    jo['params']['Transactions'] = [tx]
    return mk_snode_rpc_dapi2_url(src, 'pay'), jo, default_rpc_req_headers()

def mk_pay_status_request(node, pay_id, block_num):
    jo = json.loads(json.dumps(RequestTemplate.pay_status))
    jo['params']['PaymentID'] = pay_id
    jo['params']['BlockNumber'] = block_num
    return mk_snode_rpc_dapi2_url(node, 'pay_status'), jo, default_rpc_req_headers()

def mk_sale_status_request(node, pay_id, block_num):
    jo = json.loads(json.dumps(RequestTemplate.sale_status))
    jo['params']['PaymentID'] = pay_id
    jo['params']['BlockNumber'] = block_num
    return mk_snode_rpc_dapi2_url(node, 'sale_status'), jo, default_rpc_req_headers()

def mk_unicast_request(src, dst):
    jo = json.loads(json.dumps(RequestTemplate.unicast))
    jo['params']['sender_address'] = src.wallet
    jo['params']['receiver_address'] = dst.wallet
    jo['params']['data'] = '{}:{}'.format(src.ip, get_hires_timestamp())

    return mk_node_rpc_rta_url_by_host(src), jo, default_rpc_req_headers()

def mk_broadcast_request(src):
    jo = json.loads(json.dumps(RequestTemplate.broadcast))
    jo['params']['sender_address'] = src.wallet
    jo['params']['data'] = '{}:{}'.format(src.ip, get_hires_timestamp())

    return mk_node_rpc_rta_url_by_host(src), jo, default_rpc_req_headers()

def mk_multicast_request(src, dst_list):
    jo = json.loads(json.dumps(RequestTemplate.multicast))
    jo['params']['sender_address'] = src.wallet
    jo['params']['data'] = '{}:{}'.format(src.ip, get_hires_timestamp())

    dst_wallets = []
    for h in dst_list:
      dst_wallets.append(h.wallet)
    jo['params']['receiver_addresses'] = dst_wallets

    return mk_node_rpc_rta_url_by_host(src), jo, default_rpc_req_headers()

def mk_transfer_rta_request(src, dst_list):
    jo = json.loads(json.dumps(RequestTemplate.transfer_rta))
    jo['params']['destinations'] = dst_list

    return mk_wallet_rpc_url_by_host(src), jo, default_rpc_req_headers()

def inc_timestamp(json_obj):
    json_obj['params']['timestamp'] = get_next_timestamp()

def set_timestamp(json_obj):
    #json_obj['params']['timestamp'] = get_current_timestamp()
    json_obj['params']['timestamp'] = get_faked_timestamp()

def adj_snode_netw_addr(json_obj, snode_ip, snode_port):
    json_obj['params']['network_address'] = mk_netw_addr(snode_ip, snode_port)

def one_request(addr, port):
    log.info('listening for a request on port {}...'.format(port))

    class RequestHandler(BaseHTTPRequestHandler):
        #def do_GET(self):
        #    health = {'status': 'ok'}
        #    self.send_response(200)
        #    self.send_header('Content-Type', 'application/json')
        #    self.end_headers()
        #    self.wfile.write(bytes(json.dumps(health), 'UTF-8'))

        def do_POST(self):
            log.info('POST arrived from {}, path: {}'.format(self.address_string(), self.path))

    httpd = HTTPServer((addr, port), RequestHandler)
    httpd.handle_request()
    httpd.server_close()
    return

def mk_file_name_by_func_ip_time(func_name, ip_addr):
    dateFmt = '%Y%m%d-%H%M-%S-%f'
    now = datetime.datetime.today()
    file_name = func_name + '-' + ip_addr .replace('.', '-')  + '-' + now.strftime(dateFmt)
    return file_name

def dump_to_file(func_name, ip_addr, text_to_dump):
    fn = mk_file_name_by_func_ip_time(func_name, ip_addr) + '.json'
    with open(fn, 'w') as outfile:
        outfile.write(text_to_dump)

def mk_announce_request(host, snode_ip, snode_port):
    jo = json.loads(json.dumps(RequestTemplate.announce))
    jo['params']['timestamp'] = get_faked_timestamp()
    jo['params']['address'] = host.wallet
    adj_snode_netw_addr(jo, snode_ip, snode_port)
    return jo

def send_announce(host, snode_ip = ip_any_local, snode_port = port_srpc):
    jo = mk_announce_request(host, snode_ip, snode_port)
    log.info('Announnce JSON to send: {}'.format(json.dumps(jo)))

    url_nrpc = mk_node_rpc_rta_url_by_host(host)
    log.info('Node RPC url: {}'.format(url_nrpc))
    r = requests.post(url_nrpc, json = jo, headers = default_rpc_req_headers())
    print(' # resp: {}'.format(r.json()))
    #print(' # resp: {}'.format(json.dumps(r.json(), indent = 2)))

def send_get_connections(ip_addr, port, snode_ip = ip_any_local, snode_port = port_srpc):
    url_nrpc = mk_node_rpc_url(ip_addr, port)
    log.info('Node RPC url: {}'.format(url_nrpc))

    json_req = {"jsonrpc":"2.0","id":"0","method":"get_connections"}
    log.info('JSON to send: {}'.format(json.dumps(json_req)))

    r = requests.post(url_nrpc, json = json_req, headers = default_rpc_req_headers())
    rs = r.content
    rs = r.text
    print(' # resp: {}'.format(rs))
    dump_to_file('get-conns', ip_addr, rs)
    #print(r.json())
    #print(' # resp: {}'.format(json.dumps(r.json(), indent = 2, ensure_ascii = False, encoding = 'utf8')))

def send_get_peer_list(ip_addr, port):
    url_nrpc = 'http://' + ip_addr + ':' + str(port) + '/get_peer_list'
    log.info('Node RPC url: {}'.format(url_nrpc))

    r = requests.get(url_nrpc, headers = default_rpc_req_headers())
    rs = json.dumps(r.json(), indent = 2)
    print(' # resp: {}'.format(rs))
    dump_to_file('get-peer-list', ip_addr, rs)

def send_get_tunnels(host, snode_ip = ip_any_local, snode_port = port_srpc):
    url_nrpc = mk_node_rpc_rta_url_by_host(host)
    log.info('Node RPC url: {}'.format(url_nrpc))

    json_req = {"jsonrpc":"2.0","id":"0","method":"get_tunnels"}
    log.info('JSON to send: {}'.format(json.dumps(json_req)))

    hdrs = {'Content-Type':'application/json'}
    r = requests.post(url_nrpc, json = json_req, headers = hdrs)
    rs = r.text
    print(' # resp: {}'.format(rs))
    dump_to_file('get-tunnels', host.ip, rs)



def send_announce_to_node(host, wait_before_send = 0):
    send_announce(host, ip_n0)

def send_unicast_request(src, dst, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_unicast_request(src, dst)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    print(' # resp: {}'.format(r.json()))

def send_broadcast_request(src, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_broadcast_request(src)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    print(' # resp: {}'.format(r.json()))

def send_multicast_request(src, dst_list, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_multicast_request(src, dst_list)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    print(' # resp: {}'.format(r.json()))

def send_sale_request(src, amount, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_sale_request(src, amount)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    print(' # resp: {}'.format(r.json()))
    return r.json()

def send_sale_details_request(src, pay_id, block_num, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_sale_details_request(src, pay_id, block_num)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    #print(' # resp: {}'.format(r.json()))
    return r.json()

def send_sale_status_request(node, pay_id, block_num, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_sale_status_request(node, pay_id, block_num)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    return r.json()

def send_pay_status_request(node, pay_id, block_num, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_pay_status_request(node, pay_id, block_num)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    return r.json()

def parse_sale_response(sale_resp):
    pass

def sale_resp_is_ok(sale_resp):
    hit = 'result' in sale_resp
    return hit

def sale_resp_is_err(sale_resp):
    hit = 'error' in sale_resp
    return hit

def sale_resp_get_result(sale_resp):
    o = sale_resp['result']
    pay_id = o['PaymentID']
    block_num = o['BlockNumber']
    return pay_id, block_num

def sale_resp_get_err(sale_resp):
    o = sale_resp['error']
    code = o['code']
    msg = o['message']
    return code, msg

def sale_datails_resp_is_ok(sd_resp):
    hit = 'result' in sd_resp
    return hit

def sale_datails_resp_is_err(sd_resp):
    hit = 'error' in sd_resp
    return hit

def sale_details_resp_get_err(sd_resp):
    o = sd_resp['error']
    code = o['code']
    msg = o['message']
    return code, msg

def pay_resp_is_ok(pay_resp):
    hit = ('result' in pay_resp) and ('Result' in pay_resp['result']) and (pay_resp['result']['Result'] == 0)
    return hit

def sale_status_is_ok(sale_status_resp):
    hit = ('result' in sale_status_resp) and ('Status' in sale_status_resp['result']) and (sale_status_resp['result']['Status'] == int(RequestTemplate.SaleStatus.success))
    return hit

def pay_status_is_ok(pay_status_resp):
    #print('pay-status-is-ok: val: {}, const: {}'.format(pay_status_resp['result']['Status'], int(RequestTemplate.PayStatus.success)))
    hit = pay_status_resp['result']['Status'] == int(RequestTemplate.PayStatus.success)
    #hit = ('result' in pay_status_resp) and ('Status' in pay_status_resp['result']) and (pay_status_resp['result']['Status'] == RequestTemplate.PayStatus.success)
    return hit

def send_transfer_rta_request(src, dst_list, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_transfer_rta_request(src, dst_list)
    log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    return r.json()

def send_pay_request(src, merchant_addr, pay_id, block_num, amount, tx, wait_before_send = 0):
    wait(wait_before_send)
    url, jo, hdrs = mk_pay_request(src, merchant_addr, pay_id, block_num, amount, tx)
    #log_url_json(url, jo)
    r = requests.post(url, json = jo, headers = hdrs)
    return r.json()

def there_is_running_graft(graft_grep_result, graft_launch_cmd):
    if graft_grep_result:
        print('grep-res: `{}`\ncmd `{}`'.format(graft_grep_result, graft_launch_cmd))
    return graft_launch_cmd in graft_grep_result

def host_is_up(host):
    graft_grep = exec_ssh_cmd(cmd_grep_graft, host)
    graft_launch_cmd = mk_shell_cmd_for_start_graftnoded(host)
    is_up = there_is_running_graft(graft_grep, graft_launch_cmd)
    print('\n  ##  host `{}` is {}'.format(host.name, ('UP' if is_up else 'Down')))
    return is_up

def mk_host_up(host):
    cmd = mk_shell_cmd_for_start_graftnoded(host)
    print('\n  ##  mk_host_up `{}`'.format(cmd))
    exec_ssh_cmd(cmd, host)

def mk_host_down(host):
    kill_host_max_attempt_cnt = 10
    cmd = cmd_node_down
    while host_is_up(host):
        exec_ssh_cmd(cmd, host)
        if host_is_up(host):
            wait(2)

def exec_send_announce_to_node_1():
    send_announce(host1, ip_n1)

def exec_send_announce_to_node_2():
    send_announce(host2, ip_n2)

def exec_send_announce_to_node_3():
    send_announce(host3, ip_n3)

def exec_send_announce_to_node_12():
    exec_send_announce_to_node_1()
    exec_send_announce_to_node_2()

def exec_send_announce_to_node_13():
    exec_send_announce_to_node_1()
    exec_send_announce_to_node_3()

def exec_send_announce_to_node_23():
    exec_send_announce_to_node_2()
    exec_send_announce_to_node_3()

def exec_send_announce_to_node_123():
    exec_send_announce_to_node_1()
    exec_send_announce_to_node_2()
    exec_send_announce_to_node_3()

def send_announce_to_node(host, wait_before_send = 0):
    wait(wait_before_send)
    send_announce(host, ip_n0)

def exec_send_announce_to_node_01():
    send_announce(host1, ip_n0)

def exec_send_announce_to_node_02():
    send_announce(host2, ip_n0)

def exec_send_announce_to_node_03():
    send_announce(host3, ip_n0)

def exec_send_announce_to_node_012():
    exec_send_announce_to_node_01()
    exec_send_announce_to_node_02()

def exec_send_announce_to_node_013():
    exec_send_announce_to_node_01()
    exec_send_announce_to_node_03()

def exec_send_announce_to_node_023():
    exec_send_announce_to_node_02()
    exec_send_announce_to_node_03()

def exec_send_announce_to_node_0123():
    exec_send_announce_to_node_01()
    exec_send_announce_to_node_02()
    exec_send_announce_to_node_03()


def exec_get_connections_to_node(ip_addr):
    send_get_connections(ip_addr, port_nrpc, ip_n0, port_srpc)

def exec_get_connections_to_node_1():
    exec_get_connections_to_node(ip_n1)

def exec_get_connections_to_node_2():
    exec_get_connections_to_node(ip_n2)

def exec_get_connections_to_node_3():
    exec_get_connections_to_node(ip_n3)

def exec_get_connections_to_node_123():
    exec_get_connections_to_node_1()
    exec_get_connections_to_node_2()
    exec_get_connections_to_node_3()

def exec_get_peer_list_of_node(ip_addr):
    send_get_peer_list(ip_addr, port_nrpc)

def exec_get_peer_list_of_node_1():
    exec_get_peer_list_of_node(ip_n1)

def exec_get_peer_list_of_node_2():
    exec_get_peer_list_of_node(ip_n2)

def exec_get_peer_list_of_node_3():
    exec_get_peer_list_of_node(ip_n3)

def exec_get_peer_list_of_node_123():
    exec_get_peer_list_of_node_1()
    exec_get_peer_list_of_node_2()
    exec_get_peer_list_of_node_3()

def exec_get_123():
    exec_get_connections_to_node_123()
    exec_get_peer_list_of_node_123()


def exec_get_tunnels_to_node(host):
    send_get_tunnels(host)

def exec_node_up_1():
    exec_ssh_cmd(cmd_node_1_up, host1)

def exec_node_up_2():
    exec_ssh_cmd(cmd_node_2_up, host2)

def exec_node_up_3():
    exec_ssh_cmd(cmd_node_3_up, host3)


def exec_node_down_1():
    exec_ssh_cmd(cmd_node_1_down, host1)

def exec_node_down_2():
    exec_ssh_cmd(cmd_node_2_down, host2)

def exec_node_down_3():
    exec_ssh_cmd(cmd_node_3_down, host3)


def send_unicast(src, dst, wait_before_send = 0):
    send_unicast_request(src, dst, wait_before_send)

def exec_send_unicast_12():
    send_unicast_request(host1, host2)

def exec_send_unicast_21():
    send_unicast_request(host2, host1)

def exec_send_unicast_13():
    send_unicast_request(host1, host3)

def exec_send_unicast_31():
    send_unicast_request(host3, host1)

def exec_send_unicast_23():
    send_unicast_request(host2, host3)

def exec_send_unicast_32():
    send_unicast_request(host3, host2)

def send_broadcast_from(host, wait_before_send = 0):
    send_broadcast_request(host, wait_before_send)

def exec_send_broadcast_1():
    send_broadcast_request(host1)

def exec_send_broadcast_2():
    send_broadcast_request(host2)

def exec_send_broadcast_3():
    send_broadcast_request(host3)

def send_multicast_from(host, host_list, wait_before_send = 0):
    dst_list = []
    for h in host_list:
        if h.ip == host.ip:
            continue
        dst_list.append(h)
    send_multicast_request(host, dst_list, wait_before_send)

def exec_send_multicast_123():
    send_multicast_request(host1, [host2, host3])

def exec_send_multicast_213():
    send_multicast_request(host2, [host1, host3])

def exec_send_multicast_312():
    send_multicast_request(host3, [host1, host2])


def exec_start_host_by_idx():
    params = cmd_line_params['0'].params
    if not params:
      sys.exit('Not enough input param')

    from host_ctl import HostCtl
    from test_run_conf import TestRunConfig
    cfg = TestRunConfig()
    cfg_file = 'conf.default.json'
    curr_path = os.path.dirname(os.path.realpath(__file__))
    load_config(curr_path, cfg_file, cfg)
    hc = HostCtl(lambda: cfg.nodes)
    host_idx = int(params[0])
    hc.start(host_idx, mk_time_stamp_for_test(), mk_remote_path_to_log_dir(cfg.nodes[host_idx]))

def exec_start_all_hosts():
    from host_ctl import HostCtl
    from test_run_conf import TestRunConfig
    cfg = TestRunConfig()
    cfg_file = 'conf.default.json'
    curr_path = os.path.dirname(os.path.realpath(__file__))
    load_config(curr_path, cfg_file, cfg)
    hc = HostCtl(lambda: cfg.nodes)
    hc.start_all2(mk_time_stamp_for_test(), mk_remote_path_to_log_dir(cfg.nodes[0]))

def exec_stop_all_hosts():
    from host_ctl import HostCtl
    from test_run_conf import TestRunConfig
    cfg = TestRunConfig()
    cfg_file = 'conf.default.json'
    curr_path = os.path.dirname(os.path.realpath(__file__))
    load_config(curr_path, cfg_file, cfg)
    hc = HostCtl(lambda: cfg.nodes)
    hc.stop_all()

    #ts = time.time()
    #print('ts: {}'.format(get_current_timestamp()))
    #cmd = 'ssh gn01 "ps aux | grep graft"'

#def exec_ssh_cmd(cmd, host):
#    rsa_key_file = ssh_pvt_key_file_name()
#    k = paramiko.RSAKey.from_private_key_file(rsa_key_file)
#    sc = paramiko.SSHClient()
#    sc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    sc.connect(hostname = host.name, username = host.user, pkey = k)
#    #sc.connect(srv, username = usr, password=password)
#    sc_stdin, sc_stdout, sc_stderr = sc.exec_command(cmd)
#
#    ssh_cmd_out = ''
#    while not sc_stdout.channel.exit_status_ready():
#        # Only print data if there is data to read in the channel
#        if sc_stdout.channel.recv_ready():
#            rl, wl, xl = select.select([ sc_stdout.channel ], [ ], [ ], 0.0)
#            if len(rl) > 0:
#                tmp = sc_stdout.channel.recv(1024)
#                #output = tmp.decode()
#                #print(output)
#                ssh_cmd_out += tmp.decode()
#    sc.close()
#    #print('\n  ## ssh-cmd-out: {}'.format(ssh_cmd_out))
#    return ssh_cmd_out

def exec_test():
    print('exec_test ...')

def exec_test_1():
    #print('h1: {}'.format(host1))
    #print('ts: {}'.format(get_hires_timestamp()))
    #print('the user is `{}`'.format(get_username()))
    #print(ssh_pvt_key_file_name())
    #print(mk_shell_param_exclusive_node_list(host1))
    #print(mk_shell_cmd_for_start_graftnoded(host2))

    mk_host_down(host1)
    time.sleep(2)

    if check_if_host_is_up(host1):
        print('\n  ## there is running graft ...')
        mk_host_down(host1)
        graft_grep = exec_ssh_cmd(cmd_grep_graft, host1)
        print('\n  ## graft-grep: {}'.format(graft_grep))
    else:
        print('\n  ## no any graft found!')

    time.sleep(2)
    mk_host_up(host1)
    time.sleep(2)

    graft_grep = exec_ssh_cmd(cmd_grep_graft, host1)
    graft_launch_cmd = mk_shell_cmd_for_start_graftnoded(host1)
    if there_is_running_graft(graft_grep, graft_launch_cmd):
        print('\n  ## there is running graft ...')
    else:
        print('\n  ## no any graft found!')
    #exec_ssh_cmd(cmd_grep_graft, host1)

def create_cmd_line_args_parser():
    ap = argparse.ArgumentParser()
    ap.add_argument('action')
    ap.add_argument('params', nargs = argparse.REMAINDER)
#required = False


    #ap.add_argument('actions1')
    return ap

scenarios = {
    'sa1':      exec_send_announce_to_node_1,
    'sa2':      exec_send_announce_to_node_2,
    'sa3':      exec_send_announce_to_node_3,
    'sa12':     exec_send_announce_to_node_12,
    'sa13':     exec_send_announce_to_node_13,
    'sa23':     exec_send_announce_to_node_23,
    'sa123':    exec_send_announce_to_node_123,

    'sa01':      exec_send_announce_to_node_01,
    'sa02':      exec_send_announce_to_node_02,
    'sa03':      exec_send_announce_to_node_03,
    'sa012':     exec_send_announce_to_node_012,
    'sa013':     exec_send_announce_to_node_013,
    'sa023':     exec_send_announce_to_node_023,
    'sa0123':    exec_send_announce_to_node_0123,

    'sgc1':     exec_get_connections_to_node_1,
    'sgc2':     exec_get_connections_to_node_2,
    'sgc3':     exec_get_connections_to_node_3,
    'sgc123':   exec_get_connections_to_node_123,

    'sgpl1':    exec_get_peer_list_of_node_1,
    'sgpl2':    exec_get_peer_list_of_node_2,
    'sgpl3':    exec_get_peer_list_of_node_3,
    'sgpl123':  exec_get_peer_list_of_node_123,

    'sg123':    exec_get_123,

    'nu1':      exec_node_up_1,
    'nu2':      exec_node_up_2,
    'nu3':      exec_node_up_3,

    'nd1':      exec_node_down_1,
    'nd2':      exec_node_down_2,
    'nd3':      exec_node_down_3,

    'sun12':    exec_send_unicast_12,
    'sun21':    exec_send_unicast_21,
    'sun13':    exec_send_unicast_13,
    'sun31':    exec_send_unicast_31,
    'sun23':    exec_send_unicast_23,
    'sun32':    exec_send_unicast_32,

    'sbr1':    exec_send_broadcast_1,
    'sbr2':    exec_send_broadcast_2,
    'sbr3':    exec_send_broadcast_3,

    'smu123':  exec_send_multicast_123,
    'smu213':  exec_send_multicast_213,
    'smu312':  exec_send_multicast_312,

    'shidx':   exec_start_host_by_idx,
    'ahup':    exec_start_all_hosts,
    'ahdn':    exec_stop_all_hosts,

    'test':     exec_test,
    't1':       exec_test_1
}

cmd_line_params = {}

def execute_command_based_on_cmd_line_argumetns():
    ap = create_cmd_line_args_parser()
    args = ap.parse_args()
    cmd_line_params['0'] = args

    print('args: {}'.format(args))

    try:
        func = scenarios[args.action]
        print("Scenario '{}' is going to execute".format(func.__name__))
        func()
    except KeyError:
        print("ERR: unknown action '{}'".format(args.action))

if __name__ == '__main__':
    execute_command_based_on_cmd_line_argumetns()

    #send_msg(announce_json_data_file_n2, ip_n2, port_nrpc)
    #send_msg(announce_json_data_file_n3, ip_n3, port_nrpc)

    #send_msg(node_2_announce_json_data_file, n2_ip, n_rpc_port)
    #send_msg(announce_json_data_file_n3, ip_n3, port_nrpc)
    #one_request('0.0.0.0', port_srpc)
    #one_request('0.0.0.0', port_srpc)

#def exec_ssh_cmd(cmd, host, user):
#    rsa_key_file = '/home/cybo/.ssh/id_rsa'
#    k = paramiko.RSAKey.from_private_key_file(rsa_key_file)
#    sc = paramiko.SSHClient()
#    sc.set_missing_host_key_policy(paramiko.AutoAddPolicy())
#    sc.connect(hostname = host, username = user, pkey = k)
#    sc_stdin, sc_stdout, sc_stderr = sc.exec_command(cmd)
#
#    while not sc_stdout.channel.exit_status_ready():
#        if sc_stdout.channel.recv_ready():
#            rl, wl, xl = select.select([ sc_stdout.channel ], [ ], [ ], 0.0)
#            if len(rl) > 0:
#                tmp = sc_stdout.channel.recv(1024)
#                output = tmp.decode()
#                print(output)
#    sc.close()

#cmd_node_1_up = '/home/ubuntu/projects/graft//bin/graftnoded --testnet --testnet-rpc-bind-port 28681 --rpc-bind-ip 0.0.0.0 --confirm-external-bind --detach --add-exclusive-node 54.197.32.149 --add-exclusive-node 52.90.236.226'
#cmd_node_2_up = '/home/ubuntu/projects/graft//bin/graftnoded --testnet --testnet-rpc-bind-port 28681 --rpc-bind-ip 0.0.0.0 --confirm-external-bind --detach --add-exclusive-node 54.226.23.229 --add-exclusive-node 52.90.236.226'
#cmd_node_3_up = '/home/ubuntu/projects/graft//bin/graftnoded --testnet --testnet-rpc-bind-port 28681 --rpc-bind-ip 0.0.0.0 --confirm-external-bind --detach --add-exclusive-node 54.226.23.229 --add-exclusive-node 54.197.32.149'

#cmd_graftnoded_up = '/home/ubuntu/projects/graft//bin/graftnoded --testnet --testnet-rpc-bind-port 28681 --rpc-bind-ip 0.0.0.0 --confirm-external-bind --detach --add-exclusive-node 54.197.32.149 --add-exclusive-node 52.90.236.226'

#cmd_graftnoded_up = '/home/ubuntu/projects/GraftNetwork/build/release/bin/graftnoded --testnet --testnet-rpc-bind-port 28681 --rpc-bind-ip 0.0.0.0 --confirm-external-bind --add-exclusive-node 54.197.32.149 --add-exclusive-node 52.90.236.226 && wait(10)'
#cmd = cmd_graftnoded_up
#cmd = cmd_grep_graft
#cmd = cmd_kill_graft


#announce_json_file = 'announce.json'
#unicast_json_file = 'unicast.json'
#broadcast_json_file = 'broadcast.json'
#multicast_json_file = 'multicast.json'

#def func(x):
#    return x + 1
#
#def test_answer():
#    assert func(3) != 5
#    print('Aloha, man!')


    #with open(mk_full_file_name_from_local_name(announce_json_file)) as jf:
    #    ss = jf.read()
    #    jo = json.loads(ss)
    #    jo['params']['timestamp'] = get_faked_timestamp()
    #    jo['params']['address'] = host.wallet
    #    adj_snode_netw_addr(jo, snode_ip, snode_port)
    #return jo



#def mk_unicast_request(src, dst):
#    with open(mk_full_file_name_from_local_name(unicast_json_file)) as jf:
#        ss = jf.read()
#        jo = json.loads(ss)
#        jo['params']['sender_address'] = src.wallet
#        jo['params']['receiver_address'] = dst.wallet
#        jo['params']['data'] = '{}:{}'.format(src.ip, get_hires_timestamp())
#
#    url = mk_node_rpc_rta_url_by_host(src)
#    hdrs = {'Content-Type':'application/json'}
#    return url, jo, hdrs




#def mk_broadcast_request(src):
#    with open(mk_full_file_name_from_local_name(broadcast_json_file)) as jf:
#        ss = jf.read()
#        jo = json.loads(ss)
#        jo['params']['sender_address'] = src.wallet
#        jo['params']['data'] = '{}:{}'.format(src.ip, get_hires_timestamp())
#
#    url = mk_node_rpc_rta_url_by_host(src)
#    hdrs = {'Content-Type':'application/json'}
#    return url, jo, hdrs
#
#def mk_multicast_request(src, dst_list):
#    with open(mk_full_file_name_from_local_name(multicast_json_file)) as jf:
#        ss = jf.read()
#        jo = json.loads(ss)
#        jo['params']['sender_address'] = src.wallet
#        jo['params']['data'] = '{}:{}'.format(src.ip, get_hires_timestamp())
#
#        dst_wallets = []
#        for h in dst_list:
#          dst_wallets.append(h.wallet)
#        jo['params']['receiver_addresses'] = dst_wallets
#
#    url = mk_node_rpc_rta_url_by_host(src)
#    hdrs = {'Content-Type':'application/json'}
#    return url, jo, hdrs


#from future.moves.urllib.parse import urlparse, parse_qs
