#!/usr/bin/python
# -*- coding:utf-8 -*-
# Created Time: Wed May  6 01:13:18 2015
# Purpose: ecard handler
# Mail: hewr2010@gmail.com
__author__ = "Wayne Ho"

from collections import namedtuple
from datetime import datetime
import re
import logging
import requests
from bs4 import BeautifulSoup
import xml.sax.saxutils as saxutils

Record = namedtuple('Record', ['location', 'type_', 'date', 'amount'])


def get_ecard_result(browser):
    url = saxutils.unescape(re.search(
        r'"(http://ecard\.tsinghua\.edu\.cn/user/Login\.do.+)"',
        browser.get(
            "http://info.tsinghua.edu.cn/render.userLayoutRootNode.uP"
        ).text
    ).group(1))
    logging.info("Ecard URL: %s" % url)
    soup = BeautifulSoup(browser.get(url).text)
    table = soup.form.div.findChild('table', recursive=False)
    trs = table.findAll('tr', recursive=False)[1:]
    result = map(lambda tr: [td.text.strip() for td in tr.findAll('td')], trs)
    return map(lambda x: Record(x[0], x[1], datetime(*map(int, x[2].split('-'))), float(x[3].strip(u'￥'))), result)

if __name__ == "__main__":
    pass
