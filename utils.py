#!/usr/bin/python
# -*- coding:utf-8 -*-
# Created Time: Wed May  6 00:22:35 2015
# Purpose: useful functions
# Mail: hewr2010@gmail.com
__author__ = "Wayne Ho"

import json
import time
from datetime import datetime, date
import requests
import smtplib
from email.mime.text import MIMEText
import argparse
parser = argparse.ArgumentParser(description='THU Notifier')
parser.add_argument("--config", "-f",
                    help="load configuration",
                    required=False,
                    default="",
                    type=str)
parser.add_argument("--log-filename", "-l",
                    help="records log",
                    required=False,
                    default=str(int(time.time())) + ".db",
                    type=str)
args = parser.parse_args()

browser = requests.session()


def lprint(content):
    print json.dumps(content, ensure_ascii=False)


def login(browser, username, password):
    browser.post(
        'https://info.tsinghua.edu.cn/Login',
        {
            'redirect': 'NO',
            'x': 0, 'y': 0,
            'userName': username,
            'password': password
        }
    )


def send_email(mail_user, mail_passwd, mail_to, smtp, subject, content):
    # configuration
    msg = MIMEText(content.encode("utf8"))
    msg['From'] = mail_user
    msg['Subject'] = subject
    msg['To'] = mail_to
    try:
        s = smtplib.SMTP()
        s.connect(smtp)
        s.login(mail_user, mail_passwd)
        s.sendmail(mail_user, [mail_to], msg.as_string())
        s.close()
    except Exception, e:
        print e

if __name__ == "__main__":
    pass
