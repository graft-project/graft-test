#!/usr/bin/env python3

import pytest
import os
from ptlibx import driver as drv
from ptlib.graft_proc import GraftProc, ProcPropsBase

ss = drv.session

@pytest.fixture
def report_ctl(request):
    ss.core.load_conf_by_current_conftest(__file__, ss.cfg)
    ss.report_ctl.start_report()
    yield
    ss.report_ctl.finalize_report()

@pytest.fixture
def host_starter(request):
    graft = GraftProc()
    ss.host_ctl.stop_all(graft.all)

    path = ss.core.mk_remote_path_to_log_dir(ss.cfg.nodes[0])
    graft.noded.pass_args_for_cmd_start(path, ss.report_ctl.time_stamp, ss.cfg.nodes)
    ss.host_ctl.start_all2([graft.noded, graft.server])

    yield
    pass

