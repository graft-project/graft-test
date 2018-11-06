#!/usr/bin/env python3

import pytest
from ptlibx import driver as drv
from ptlib.snode_stub import SNodeStub as SNodeStub
from flask import json, request

ss = drv.session

def check_result(resp_list, peer_sender, peer_subj):
    found = False
    for r in resp_list:
        if r['flask_remote_addr'] != peer_sender.ip:
            continue
        if r['params']['address'] != peer_subj.wallet:
            continue
        found = True
        break
    return found

@pytest.mark.skip(reason = 'skip')
def test(report_ctl, host_starter):
    tn = 'sale-sale-details'
    print('\n  ##  {} test is beginning ...'.format(tn))

    #ss.host_requester.get_tunnels()

    ns = SNodeStub(tn)

    @ns.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
    def on_req():
        return ns.build_custom_default_response()

    ns.run()

    for host in ss.cfg.nodes:
        ss.core.send_announce_to_node(host, ss.cfg.wait['between_announces'])

    #ss.host_requester.get_tunnels()

    time.sleep(ss.cfg.wait['between_announces'])
    received = len(ns.resp_list)
    print('\n  ##  reqs done by now: {}'.format(received))

    ns.cnt_resp_to_collect = received + ss.cfg.count_of_arrangement()

    #ss.host_requester.get_tunnels()
    for host in ss.cfg.nodes:
        ss.core.send_announce_to_node(host, ss.cfg.wait['between_test_request'])
        #ss.host_requester.get_tunnels()

    ns.wait_till_complete(3)

    print('{}'.format(json.dumps(ns.resp_list, indent = 2)))

    for src in ss.cfg.nodes:
        for dst in ss.cfg.nodes:
            if src.ip == dst.ip:
                continue
            print('from {} about {}: {}'.format(src.name, dst.name, check_result(ns.resp_list, src, dst)))

    for src in ss.cfg.nodes:
        for dst in ss.cfg.nodes:
            if src.ip == dst.ip:
                continue
            assert check_result(ns.resp_list, src, dst)


