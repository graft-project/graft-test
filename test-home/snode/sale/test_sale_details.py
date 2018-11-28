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

def cond_sale(host_name):
    req = 'sale'
    return host_name + '-' + req

def cond_sale_det(host_name, host_name2):
    req = 'sail-details'
    return host_name + '-' + req + '-' + host_name2

@pytest.mark.skip(reason = 'skip')
def test_dbg(report_ctl, host_starter):
    tn = 'sale-sale-details-DBG'
    print('\n  ##  {} test is beginning ...'.format(tn))

    #p = 10
    #p2 = 5
    #p3 = 10

    ss.core.wait(ss.cfg.wait['before_start_mining'])
    ss.host_ctl.mining_start(ss.graft_proc.noded)
    ss.core.wait(ss.cfg.wait['after_start_mining'])

    amount = 500 * 1000
    check_list = set()
    for h in ss.cfg.nodes:
        print('\n\n  ================ sale for {}'.format(h.name))
        sale_resp = ss.core.send_sale_request(h, amount, 1)
        if ss.core.sale_resp_is_ok(sale_resp):
            check_list.add(cond_sale(h.name))
            print('  ##  sale-resp for {} is OK'.format(h.name))
            pay_id, block_num = ss.core.sale_resp_get_result(sale_resp)
            for hh in ss.cfg.nodes:
                print('\n  ================ sale-datails for {} about {}'.format(hh.name, h.name))
                for try_cnt in range(0, 4):

                    if try_cnt == 0:
                        ss.core.wait(p2)
                    else:
                        ss.core.wait(p3)

                    sd_resp = ss.core.send_sale_details_request(hh, pay_id, block_num)
                    if ss.core.sale_datails_resp_is_ok(sd_resp):
                        print('sale-details-resp for {} - OK'.format(hh.name))
                        check_list.add(cond_sale_det(h.name, hh.name))
                        break
                    else:
                        ec, em = ss.core.sale_details_resp_get_err(sd_resp)
                        print('sale-details-resp ERR-{}: {} {}'.format(try_cnt, ec, em))

        elif ss.core.sale_resp_is_err(sale_resp):
            ec, em = ss.core.sale_resp_get_err(sale_resp)
            print('sale-resp ERR: {} {}'.format(ec, em))

    for x in check_list:
          print(x)

    for h in ss.cfg.nodes:
        assert (cond_sale(h.name) in check_list)
        for hh in ss.cfg.nodes:
            assert (cond_sale_det(h.name, hh.name) in check_list)


