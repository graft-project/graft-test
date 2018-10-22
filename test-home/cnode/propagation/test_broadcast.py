#!/usr/bin/env python3

import pytest
from ptlibx import driver as drv
from ptlib.snode_stub import SNodeStub as SNodeStub
import time
from flask import json, request

def check_result(resp_list, peer_src, peer_dst):
    found = False
    for r in resp_list:
        if not 'data' in r['params']:
            continue
        if r['params']['data'].split(':')[0] != peer_src.ip:
            continue
        if r['flask_remote_addr'] != peer_dst.ip:
            continue
        found = True
        break
    return found

#@pytest.mark.skip(reason = 'skip')
def test(host_ctl):
    tn = 'broadcast'
    print('\n  ##  {} test is beginning ...'.format(tn))

    p1 = 2
    p2 = 2

    p1 = 15
    p2 = 5

    p1 = 10
    p2 = 3

    ns = SNodeStub(tn)

    @ns.route('/dapi/v2.0/broadcast', methods=['POST'])
    def on_req():
        return ns.build_custom_default_response()

    @ns.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
    def on_announce():
        return ns.build_custom_default_response()

    ns.run()

    for host in drv.core().env_desc:
        time.sleep(p1)
        drv.core().send_announce_to_node(host)

    time.sleep(p1)
    received = len(ns.resp_list)
    print('\n  ##  reqs done by now: {}'.format(received))

    ns.cnt_resp_to_collect = received + 9

    for host in drv.core().env_desc:
        time.sleep(p2)
        drv.core().send_broadcast_from(host)

    ns.wait_till_complete(3)

    print('{}'.format(json.dumps(ns.resp_list, indent = 2)))

    for src in drv.core().env_desc:
        for dst in drv.core().env_desc:
            print('{} --> {}: {}'.format(src.name, dst.name, check_result(ns.resp_list, src, dst)))

    for src in drv.core().env_desc:
        for dst in drv.core().env_desc:
            assert check_result(ns.resp_list, src, dst)


