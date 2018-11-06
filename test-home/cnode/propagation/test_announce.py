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
def test_dbg(report_ctl, host_starter):
    print('dbg-test-session is taking off ...')
    #for host in ss.env.hosts:
    #    print('host [{}]'.format(host.name))

    #print(ss.host_log_collector.name())
    print('report-ctl-current-test-name [{}]'.format(ss.report_ctl.current_report_name))
    #print('report-ctl-time-stamp [{}]'.format(ss.report_ctl.time_stamp))
    print('report-ctl-home-path [{}]'.format(ss.report_ctl.report_home_path))
    #print('report-ctl-current-test-log-path [{}]'.format(ss.report_ctl.current_report_log_path))
    #print('report-ctl-current-test-requests-path [{}]'.format(ss.report_ctl.current_report_requests_path))

    #ss.core.exec_get_123()
    #ss.core.exec_get_tunnels_to_node(ss.env.hosts[0])

    #ss.host_requester.get_tunnels()
    #print('arng-cnt: {}:{}'.format(ss.cfg.count_of_arrangement(), ss.cfg.count_of_arrangement_with_self()))

    #ss.host_log_collector.prepare_log_capture(ss.env.hosts)

    #ss.host_log_collector.put(ss.env.hosts[0])
    #ss.host_log_collector.unpack()

    #for src in ss.env.hosts:
    #    for dst in ss.env.hosts:
    #        if src.ip == dst.ip:
    #            continue
    #        print('from {} about {}: {}'.format(src.name, dst.name, check_result([], src, dst)))


@pytest.mark.skip(reason = 'skip')
def test(report_ctl, host_starter):
    tn = 'announce'
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

    ns.wait(ss.cfg.wait['between_announces'])
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


#"between_announces": "10",
#"between_test_request": "3"
#p1 = 20
#p2 = 15
#
#p1 = 15
#p2 = 10
#
#p1 = 10
#p2 = 3
#tn = NTD.get_test_name(__file__)

