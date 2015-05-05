#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by i@BlahGeek.com at 2015-04-05

import datetime
from peewee import SqliteDatabase, Model
from peewee import CharField, DateTimeField, FloatField
import utils

db = SqliteDatabase(utils.args.log_filename)

class BaseModel(Model):
    class Meta:
        database = db

class Record(BaseModel):
    location = CharField()
    type_ = CharField()
    date = DateTimeField()
    amount = FloatField()

    created_date = DateTimeField(default=datetime.datetime.now)

