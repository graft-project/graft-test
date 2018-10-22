#!/usr/bin/env python3

import pytest
import os
from ptlibx import driver as drv

ss = drv.session

@pytest.fixture(scope = 'session', autouse = True)
def session_ctl(request):
    print('\nsession_ctl started ...')

@pytest.fixture
def host_ctl(request):
    hosts = ss.env.hosts
    for h in hosts:
        ss.core.mk_host_down(h)
        ss.core.mk_host_up(h)
    yield
    pass

@pytest.fixture
def report_ctl(request):
    ss.env.hosts = ss.core.load_env_descr_by_current_conftest(__file__)
    ss.report_ctl.start_report()
    yield
    ss.report_ctl.finalize_report()


