# -*- coding: utf-8 -*-
from .api import (
    get_info_from_iptaobao,
    get_info_from_pconline,
    get_info_from_ip138,
    get_info_from_ipapi
)

from .tools import try_decorator


@try_decorator
def try_get_info_from_iptaobao(ip):
    res = get_info_from_iptaobao(ip)

    return {
        'country': res['country'],
        'city': res['city'],
        'region': res['region'],
        'isp': res['isp']
    }


@try_decorator
def try_get_info_from_pconline(ip):
    res = get_info_from_pconline(ip)

    return {
        'country': '',
        'city': res['city'],
        'region': res['pro'],
        'isp': res['addr']
    }


@try_decorator
def try_get_info_from_ipapi(ip):
    res = get_info_from_ipapi(ip)

    return {
        'country': res['country'],
        'city': res['city'],
        'region': res['regionName'],
        'isp': res['isp']
    }


@try_decorator
def try_get_info_from_ip138(ip):
    res = get_info_from_ip138(ip)

    return {
        'country': res['ct'],
        'city': res['city'],
        'region': res['prov'],
        'isp': res['yunyin']
    }
