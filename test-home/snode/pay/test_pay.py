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

#@pytest.mark.skip(reason = 'skip')
def get_neighbour_node(node_idx):
    cnt = len(ss.cfg.nodes)
    idx = (node_idx + 1) % cnt
    #print('{} - {}'.format(node_idx, idx))
    return ss.cfg.nodes[idx]

#def test_dbg_1(load_cfg):
#@pytest.mark.skip(reason = 'skip')
def test_dbg_1(report_ctl, host_starter):
    node_cnt = len(ss.cfg.nodes)
    for i in range(node_cnt):
        h = ss.cfg.nodes[i]
        hn = get_neighbour_node(i)
        print('this node: [{}], node-neighbout [{}]'.format(h, hn))

    ss.host_requester.get_tunnels()

@pytest.mark.skip(reason = 'skip')
def test_dbg(report_ctl, host_starter):
    tn = 'pay-DBG'
    print('\n  ##  {} test is beginning ...'.format(tn))

    ss.core.wait(ss.cfg.wait['before_start_mining'])
    ss.host_ctl.mining_start(ss.graft_proc.noded)
    ss.core.wait(ss.cfg.wait['after_start_mining'])

    total_amount = 300 * 1000 * 1000 * 1000

    check_list = set()
    node_cnt = len(ss.cfg.nodes)
    for i in range(node_cnt):
        h = ss.cfg.nodes[i]
        hn = get_neighbour_node(i)
        print('\n\n  ================ sale for {}'.format(h.name))
        sale_resp = ss.core.send_sale_request(h, total_amount, ss.cfg.wait['before_sale_request'])
        pay_id, block_num = ss.core.sale_resp_get_result(sale_resp)

        sd_resp = ss.core.send_sale_details_request(hn, pay_id, block_num, ss.cfg.wait['before_sale_details_request'])
        if ss.core.sale_datails_resp_is_ok(sd_resp):

            for r in sd_resp['result']['AuthSample']:
                print('{}'.format(r))

            total_fee = 0
            pay_dst_list = []
            for r in sd_resp['result']['AuthSample']:
                pay_dst_list.append({'amount':int(r['Fee']), 'address':r['Address']})
                total_fee += int(r['Fee'])

            print('\nTotal auth-fee:{}'.format(total_fee))

            pay_dst_list.append({'amount':total_amount - total_fee, 'address':h.wallet})

            for r in pay_dst_list:
                print('{}'.format(r))

            tra_resp = ss.core.send_transfer_rta_request(h, pay_dst_list, ss.cfg.wait['before_transfer_rta_request'])
            #print('transfer-rta-resp:{}'.format(tra_resp))

            pay_resp = ss.core.send_pay_request(h, ss.cfg.nodes[0].wallet, pay_id, block_num, total_amount - total_fee, tra_resp['result']['tx_blob'], ss.cfg.wait['before_pay_request'])
            #print('pay-resp: [{}]'.format(pay_resp))
            if ss.core.pay_resp_is_ok(pay_resp):
                print(' **  Pay is OK')

                pay_status_resp = ss.core.send_pay_status_request(h, pay_id, block_num, ss.cfg.wait['before_pay_status_request'])
                if ss.core.pay_status_is_ok(pay_status_resp):
                    print(' **  PayStatus is OK')
                else:
                    print('pay_status: [{}]'.format(pay_status_resp))

                sale_status_resp = ss.core.send_sale_status_request(h, pay_id, block_num, ss.cfg.wait['before_sale_status_request'])
                if ss.core.sale_status_is_ok(sale_status_resp):
                    print(' **  SaleStatus is OK')
                else:
                    print('sale_status: [{}]'.format(sale_status_resp))

                if ss.core.pay_status_is_ok(pay_status_resp) and ss.core.sale_status_is_ok(sale_status_resp):
                    check_list.add(h.name)

                #def send_pay_request(src, merchant_addr, pay_id, block_num, amount, tx, wait_before_send = 0):

    for h in ss.cfg.nodes:
        assert (h.name in check_list)

def do_not_use_it():
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


@pytest.mark.skip(reason = 'skip')
def test_sail_details_dbg(report_ctl, host_starter):
    tn = 'sail-details-DBG'
    print('\n  ##  {} test is beginning ...'.format(tn))

    p = 10
    p2 = 5
    p3 = 10
    ss.core.wait(p)
    ss.host_ctl.mining_start(ss.graft_proc.noded)
    ss.core.wait(p)

    check_list = set()
    for h in ss.cfg.nodes:
        print('\n\n  ================ sale for {}'.format(h.name))
        sale_resp = ss.core.send_sale_request(h, 1)
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


@pytest.mark.skip(reason = 'skip')
def test(report_ctl, host_starter):
    tn = 'sale-sale-details'
    print('\n  ##  {} test is beginning ...'.format(tn))

    ns = SNodeStub(tn)

    @ns.route('/dapi/v2.0/send_supernode_announce', methods=['POST'])
    def on_req():
        return ns.build_custom_default_response()

    ns.run()

    for host in ss.cfg.nodes:
        ss.core.send_announce_to_node(host, ss.cfg.wait['between_announces'])

    ns.wait(ss.cfg.wait['between_announces'])
    received = len(ns.resp_list)
    print('\n  ##  reqs done by now: {}'.format(received))

    ns.cnt_resp_to_collect = received + ss.cfg.count_of_arrangement()

    for host in ss.cfg.nodes:
        ss.core.send_announce_to_node(host, ss.cfg.wait['between_test_request'])

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


