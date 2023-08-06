# -*- coding: utf-8 -*-
import time
import unittest
from pprint import pprint

from ip_area import (
    get_info_from_ip138,
    get_info_from_iptaobao,
    get_info_from_ipapi,
    get_info_from_pconline,
    get_info
)


def timer(func):
    def decorator(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print(end - start)
        return res

    return decorator


class Test(unittest.TestCase):
    @timer
    def test_get_info_from_ip138(self):
        """3.3 0.2 0.2 0.2"""
        pprint(get_info_from_ip138('39.97.246.76'))

    @timer
    def test_get_info_from_iptaobao(self):
        """0.1 0.07 0.07 0.1"""
        pprint(get_info_from_iptaobao('39.97.246.76'))

    @timer
    def test_get_info_from_ipapi(self):
        """0.4 1.9 0.5 0.4"""
        pprint(get_info_from_ipapi('39.97.246.76'))

    @timer
    def test_get_info_from_pconline(self):
        """0.1 0.1 0.1 0.1"""
        pprint(get_info_from_pconline('39.97.246.76'))

    @timer
    def test_get_info(self):
        pprint(get_info('39.97.246.76'))