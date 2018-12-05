#!/usr/bin/env python3

import pytest
import os
from ptlibx import driver as drv

ss = drv.session

@pytest.fixture
def load_cfg(request):
    ss.core.load_conf_by_current_conftest(__file__, ss.cfg)
    yield
    pass

@pytest.fixture
def report_ctl(request):
    ss.core.load_conf_by_current_conftest(__file__, ss.cfg)
    ss.report_ctl.start_report()
    yield
    ss.report_ctl.finalize_report()

@pytest.fixture
def host_starter(request):
    ss.host_ctl.stop_all(ss.graft_proc.all)
    path = ss.core.mk_remote_path_to_log_dir(ss.cfg.nodes[0])
    ss.graft_proc.noded.pass_args_for_cmd_start(path, ss.report_ctl.time_stamp, ss.cfg.nodes)
    ss.host_ctl.start_all2([ss.graft_proc.noded, ss.graft_proc.server])
    ss.core.wait(5)
    ss.host_ctl.start_all2([ss.graft_proc.wallet_rpc])
    yield
    pass

@pytest.fixture
def start_cryptonode(request):
    ss.host_ctl.stop_all(ss.graft_proc.all)
    path = ss.core.mk_remote_path_to_log_dir(ss.cfg.nodes[0])
    ss.graft_proc.noded.pass_args_for_cmd_start(path, ss.report_ctl.time_stamp, ss.cfg.nodes)
    ss.host_ctl.start_all2([ss.graft_proc.noded])
    yield
    pass

@pytest.fixture
def start_cryptonode_and_supernode(request):
    ss.host_ctl.stop_all(ss.graft_proc.all)
    path = ss.core.mk_remote_path_to_log_dir(ss.cfg.nodes[0])
    ss.graft_proc.noded.pass_args_for_cmd_start(path, ss.report_ctl.time_stamp, ss.cfg.nodes)
    ss.host_ctl.start_all2([ss.graft_proc.noded, ss.graft_proc.server])
    yield
    pass

