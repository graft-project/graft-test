#!/usr/bin/env python3

import pytest
import os
from ptlibx import driver as drv

ss = drv.session

#@pytest.fixture(scope = 'session', autouse = True)
#def session_ctl(request):
#    print('\nsession_ctl started ...')

@pytest.fixture
def report_ctl(request):
    ss.core.load_conf_by_current_conftest(__file__, ss.cfg)
    ss.report_ctl.start_report()
    yield
    ss.report_ctl.finalize_report()

@pytest.fixture
def host_starter(request):
    ss.host_ctl.stop_all(ss.graft_proc.all)
    #ss.host_ctl.start_all2([graft.server])
    #hc.start(host_idx, mk_time_stamp_for_test(), mk_remote_path_to_log_dir(cfg.nodes[host_idx]))
    path = ss.core.mk_remote_path_to_log_dir(ss.cfg.nodes[0])
    ss.graft_proc.noded.pass_args_for_cmd_start(path, ss.report_ctl.time_stamp, ss.cfg.nodes)
    ss.host_ctl.start_all2([ss.graft_proc.noded])

#, graft.noded
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



    #print(len(ss.cfg.nodes))

    #ppb = ProcPropsBase('name')
    #ppb.host = ss.cfg.nodes[0]
    #pph = ppb.host
    #print(pph)
    #print(ppb.host)

    #x1 = graft.noded

    #print(x1)
    #print(graft.noded)
    #print(graft.wallet_cli)
