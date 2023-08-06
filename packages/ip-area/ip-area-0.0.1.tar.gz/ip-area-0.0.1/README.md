# IP Area

![PyPI](https://img.shields.io/pypi/v/ip-area.svg)
![PyPI - Downloads](https://img.shields.io/pypi/dm/ip-area)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ip-area)
![PyPI - License](https://img.shields.io/pypi/l/ip-area)


pypi: [https://pypi.org/project/scrapy-util](https://pypi.org/project/ip-area)

github: [https://github.com/mouday/scrapy-util](https://github.com/mouday/ip-area)

整合了ip地址信息的几个网站，依次作为备用：

1. 淘宝IP地址库：[http://ip.taobao.com/instructions](http://ip.taobao.com/instructions)
2. 太平洋IP地址库：[http://whois.pconline.com.cn/](http://whois.pconline.com.cn/)
3. IP-API： [https://ip-api.com/docs](https://ip-api.com/docs)
4. IP138：[https://www.ip138.com/](https://www.ip138.com/)
 
install

```
pip install ip-area
```

Demo

```python
# -*- coding: utf-8 -*-

from ip_area import get_info

print(get_info('39.97.246.76'))

"""
输出json对象
{
    'country': '中国',
    'region': '北京', 
    'city': '北京', 
    'isp': '阿里云'
}
"""
```