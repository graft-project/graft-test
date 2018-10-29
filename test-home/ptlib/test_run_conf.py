#!/usr/bin/env python3

from math import factorial, pow

class TestRunConfig(object):
    def __init__(self):
        self.__nodes = []
        self.__wait = {}

    @property
    def nodes(self):
        return self.__nodes

    @nodes.setter
    def nodes(self, val):
        self.__nodes = val

    @property
    def wait(self):
        return self.__wait

    @wait.setter
    def wait(self, val):
        self.__wait = val

    def count_of_arrangement(self):
        n = len(self.nodes)
        m = 2
        cnt = factorial(n) / factorial(n - m)
        return int(cnt)

    def count_of_arrangement_with_self(self):
        n = len(self.nodes)
        m = 2
        return int(pow(n, m))

