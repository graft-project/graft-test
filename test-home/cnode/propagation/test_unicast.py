#!/usr/bin/env python3

import pytest
from ptlibx import driver as drv
from ptlib.snode_stub import SNodeStub as SNodeStub
from flask import json, request

ss = drv.session

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
def test(report_ctl, host_starter):
    tn = 'unicast'
    print('\n  ##  {} test is beginning ...'.format(tn))

    ns = SNodeStub(tn)

    @ns.route('/dapi/v2.0/unicast', methods=['POST'])
    def on_req():
        return ns.build_custom_default_response()

    @ns.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
    def on_announce():
        return ns.build_custom_default_response()

    ns.run()

    for host in ss.cfg.nodes:
        ss.core.send_announce_to_node(host, ss.cfg.wait['between_announces'])

    ns.wait(ss.cfg.wait['between_announces'])
    received = len(ns.resp_list)
    print('\n  ##  reqs done by now: {}'.format(received))

    ns.cnt_resp_to_collect = received + ss.cfg.count_of_arrangement()

    for src in ss.cfg.nodes:
        for dst in ss.cfg.nodes:
            if src.ip == dst.ip:
                continue
            ss.core.send_unicast(src, dst, ss.cfg.wait['between_test_request'])

    ns.wait_till_complete(3)

    print('{}'.format(json.dumps(ns.resp_list, indent = 2)))

    for src in ss.cfg.nodes:
        for dst in ss.cfg.nodes:
            if src.ip == dst.ip:
                continue
            print('{} --> {}: {}'.format(src.name, dst.name, check_result(ns.resp_list, src, dst)))

    for src in ss.cfg.nodes:
        for dst in ss.cfg.nodes:
            if src.ip == dst.ip:
                continue
            assert check_result(ns.resp_list, src, dst)


