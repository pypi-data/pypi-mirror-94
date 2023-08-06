# -*- coding: utf-8 -*-

import json
import re

import requests

headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36'
}


def get_info_from_ip138(ip, timeout=2):
    """
    https://www.ip138.com/
    :param timeout:
    :param ip:
    :return:
    {
     'area': '',
     'begin': 660602880,
     'city': '北京市',
     'ct': '中国',
     'end': 660733951,
     'idc': '',
     'net': '数据中心',
     'prov': '北京市',
     'yunyin': '阿里云'
    }
    """
    url = 'https://www.ip138.com/iplookup.asp'

    params = {
        'ip': ip,
        'action': '2'
    }

    res = requests.get(url, headers=headers, timeout=timeout, params=params)

    res.encoding = res.apparent_encoding
    ret = re.search(r'var ip_result = ({.*});', res.text)
    return json.loads(ret.group(1))['ip_c_list'][0]


def get_info_from_ipapi(ip, timeout=2):
    """
    IP-API接口 https://ip-api.com/
    :param timeout:
    :param ip:
    :return:
    {
     'as': 'AS37963 Hangzhou Alibaba Advertising Co.,Ltd.',
     'city': '西湖',
     'country': '中国',
     'countryCode': 'CN',
     'isp': 'Hangzhou Alibaba Advertising Co',
     'lat': 30.2813,
     'lon': 120.12,
     'org': 'Aliyun Computing Co., LTD',
     'query': '39.97.246.76',
     'region': 'ZJ',
     'regionName': '浙江省',
     'status': 'success',
     'timezone': 'Asia/Shanghai',
     'zip': ''}
    """
    url = 'http://ip-api.com/json/' + ip
    params = {
        'lang': 'zh-CN'
    }

    res = requests.get(url, params=params, timeout=timeout, headers=headers)
    return res.json()


def get_info_from_pconline(ip, timeout=2):
    """
    太平洋IP查询 http://whois.pconline.com.cn/
    :param timeout:
    :param ip:
    :return:

    {'addr': '北京市 电信',
     'city': '北京市',
     'cityCode': '110000',
     'err': '',
     'ip': '39.97.246.76',
     'pro': '北京市',
     'proCode': '110000',
     'region': '',
     'regionCode': '0',
     'regionNames': ''}
    """
    url = 'http://whois.pconline.com.cn/ipJson.jsp'

    params = {
        'ip': ip,
        'json': 'true'
    }
    res = requests.get(url, params=params, timeout=timeout, headers=headers)
    return res.json()


def get_info_from_iptaobao(ip, timeout=2):
    """
    淘宝ip地址库 http://ip.taobao.com

    :param timeout:
    :param ip:
    :return:
    {
     'area': '',
     'area_id': '',
     'city': '北京',
     'city_id': '110100',
     'country': '中国',
     'country_id': 'CN',
     'county': '',
     'county_id': None,
     'ip': '39.97.246.76',
     'isp': '阿里云',
     'isp_id': '1000323',
     'queryIp': '39.97.246.76',
     'region': '北京',
     'region_id': '110000'
    }
    """
    url = 'http://ip.taobao.com/outGetIpInfo'

    params = {
        'ip': ip,
        'accessKey': 'alibaba-inc'
    }
    res = requests.get(url, params=params, timeout=timeout, headers=headers)
    return res.json()['data']
