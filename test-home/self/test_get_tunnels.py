#!/usr/bin/env python3

import pytest
from ptlibx import driver as drv
from ptlib.snode_stub import SNodeStub as SNodeStub
from flask import json, request

ss = drv.session

#@pytest.mark.skip(reason = 'skip')
def test_get_tunnels(report_ctl, start_cryptonode):
    tn = 'self-test -- host_requester.get_tunnels'
    print('\n  ##  {} test is beginning ...'.format(tn))

    ns = SNodeStub('get-tunnels')

    @ns.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
    def on_req():
        return ns.build_custom_default_response()

    ns.run()

    for host in ss.cfg.nodes:
        ss.core.send_announce_to_node(host, ss.cfg.wait['between_announces'])

    #ns.wait_till_complete(1)

    ss.host_requester.get_tunnels('self-test of get-tunnels', 2)
    ss.host_requester.get_peer_list('self-test of peer-list', 2)
    ss.host_requester.get_connections('self-test of get-connections', 2)

