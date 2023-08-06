# -*- coding: utf-8 -*-
from .wrap_api import (
    try_get_info_from_iptaobao,
    try_get_info_from_pconline,
    try_get_info_from_ip138,
    try_get_info_from_ipapi
)


def get_info(ip):
    """整合所有获取方式，增加容错, 统一的返回格式
    :return
    {
        'city': '北京',
        'country': '中国',
        'isp': '阿里云',
        'region': '北京'
    }
    """
    res = try_get_info_from_iptaobao(ip)
    if not res:
        res = try_get_info_from_pconline(ip)
    if not res:
        res = try_get_info_from_ip138(ip)
    if not res:
        res = try_get_info_from_ipapi(ip)
    return res
