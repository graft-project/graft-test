#!/usr/bin/env python3

import pytest
import os
from ptlibx import driver as drv
from ptlib.host_ctl import GraftProc, ProcPropsBase

ss = drv.session

#@pytest.fixture(scope = 'session', autouse = True)
#def session_ctl(request):
#    print('\nsession_ctl started ...')

@pytest.fixture
def report_ctl(request):
    ss.core.load_conf_by_current_conftest(__file__, ss.cfg)
    #ss.report_ctl.start_report()
    yield
    #ss.report_ctl.finalize_report()

@pytest.fixture
def host_starter(request):

    print(len(ss.cfg.nodes))

    ppb = ProcPropsBase('name')
    ppb.host = ss.cfg.nodes[0]
    pph = ppb.host
    print(pph)
    print(ppb.host)

    graft = GraftProc()
    x1 = graft.noded

    print(x1)
    print(graft.noded)
    print(graft.wallet_cli)

    ss.host_ctl.stop_all(graft.wallet_cli)
    #ss.host_ctl.start_all()
    yield
    pass

#@pytest.fixture
#def host_ctl(request):
#    hosts = ss.cfg.nodes
#    for h in hosts:
#        ss.core.mk_host_down(h)
#        ss.core.mk_host_up(h)
#    yield
#    pass



