#!/usr/bin/python
# -*- coding:utf-8 -*-
# Created Time: Tue May  5 23:53:34 2015
# Purpose: Main process for a notifier
# Mail: hewr2010@gmail.com
__author__ = "Wayne Ho"

import getpass
import ecard
from utils import *
from db import Record
from apscheduler.schedulers.blocking import BlockingScheduler
import logging
logging.basicConfig(level=logging.DEBUG)


def collect_ecard(browser, username, password):
    records = ecard.get_ecard_result(browser)
    logging.info('Found %d records' % len(records))
    exists_records = list(Record.select().order_by(Record.created_date.desc())
                          .limit(len(records)))
    # Maybe there's less records in db
    exists_records += [None, ] * (len(records) - len(exists_records))
    eq = lambda x, y: x is not None and y is not None and all(getattr(x, key) == getattr(y, key) for key in ecard.Record._fields)
    delta = 0
    while delta < len(records):
        if all([eq(records[i+delta], exists_records[i]) for i in range(len(records) - delta)]):
            break
        delta += 1
    logging.info('...%d of them are new to me, insert it' % delta)
    for record in records[:delta][::-1]:  # insert oldest record first
        Record.create(**record.__dict__)


def notify(email, template):
    today = datetime.today()
    records = Record.select().where(Record.date == datetime(today.year, today.month, today.day),
                                    Record.type_ == u'消费')
    total_amount = sum(map(lambda x: x.amount, records))
    logging.info('Total amount for today (%s): %.1f' % (today.strftime('%Y-%m-%d'), total_amount))
    subject = u"%s校园卡消费情况" % today.strftime('%Y-%m-%d')
    content = template % total_amount
    content += "\n" + "\n".join(map(lambda x: x.location + "\t" + str(x.amount), records))
    logging.info('Subject: %s' % subject)
    logging.info('Content: %s' % content)
    with open("email.conf") as fin:
        mail_user = fin.readline()[:-1]
        mail_passwd = fin.readline()[:-1]
        smtp = fin.readline()[:-1]
    send_email(mail_user, mail_passwd, email, smtp, subject, content)

if __name__ == "__main__":
    if args.config == "":
        username = raw_input("THU Account:\t")
        email = raw_input("Email:\t\t")
        password = getpass.getpass("Password:\t")
        template = u"今天你的校园卡一共刷了%.2f块钱~"
    else:
        account = __import__(args.config)
        username = account.username
        email = account.email
        password = account.password
        template = account.template
        #password = getpass.getpass()
    Record.create_table(fail_silently=True)
    login(browser, username, password)
    #collect_ecard(browser, username, password)
    #notify(email, template)
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_ecard, 'interval', (browser, username, password),
                      seconds=3600*6, timezone='Asia/Shanghai')
    scheduler.add_job(notify, 'cron', (email, template),
                      hour=23, minute=00, timezone='Asia/Shanghai')
    logging.info('Starting scheduler...')
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass
