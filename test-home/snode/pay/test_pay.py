#!/usr/bin/env python3

import pytest
from ptlibx import driver as drv

ss = drv.session

def get_neighbour_node(node_idx):
    cnt = len(ss.cfg.nodes)
    idx = (node_idx + 1) % cnt
    #print('{} - {}'.format(node_idx, idx))
    return ss.cfg.nodes[idx]

#@pytest.mark.skip(reason = 'skip')
def test(report_ctl, host_starter):
    tn = 'pay'
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

    for h in ss.cfg.nodes:
        assert (h.name in check_list)

