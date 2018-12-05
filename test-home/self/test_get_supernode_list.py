#!/usr/bin/env python3

import pytest
from ptlibx import driver as drv
from ptlib.snode_stub import SNodeStub as SNodeStub
from flask import json, request

ss = drv.session

#@pytest.mark.skip(reason = 'skip')
def test_get_supernode_list(report_ctl, start_cryptonode_and_supernode):
    tn = 'self-test -- host_requester.supernode-list'
    print('\n  ##  {} test is beginning ...'.format(tn))

    print('waiting 5 secs ...')
    ss.host_requester.get_supernode_all_list('self-test of get-supernode-all-list', 5)

    print('waiting 5 secs ...')
    ss.host_requester.get_supernode_good_list('self-test of get-supernode-good-list', 5)

