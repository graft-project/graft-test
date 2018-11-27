#!/usr/bin/env python3

def locate_core_ptlib():
    import os, sys
    root_marker_file = 'graft-ptlib-root'

    def find_root_ptlib_at_this_dir(path):
        tail = 'ptlib/{}'.format(root_marker_file)
        file_to_check = os.path.join(path, tail)
        return os.path.exists(file_to_check) and os.path.isfile(file_to_check)

    curr_path = os.path.dirname(os.path.realpath(__file__))

    while (len(curr_path) > 2) and not find_root_ptlib_at_this_dir(curr_path):
        curr_path = os.path.dirname(curr_path)

    if find_root_ptlib_at_this_dir(curr_path):
        sys.path.insert(0, curr_path)
        print('{} is found at [{}]'.format(root_marker_file, curr_path))
    else:
        sys.exit('ptlib not found')
    return curr_path

tests_root_path = locate_core_ptlib()

from ptlib.test_session import TestSession

session = TestSession(tests_root_path)

