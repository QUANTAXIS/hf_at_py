# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2017/11/16'
"""

from py_at.strategy import Strategy
from py_at.enums import IntervalType
from py_at.data import Data
from py_at.tick import Tick
from py_at.bar import Bar


class Test(Strategy):
    ''''''

    def __init__(self):
        super().__init__()
        data = self.Datas[0]
        data.Instrument = 'rb1805'
        data.Interval = 1
        data.IntervalType = IntervalType.Minute
        self.BeginDate = '20171111'

    def BarUpdate(self, data=Data, bar=Bar):
        if self.Tick.Instrument == '':
            return
        if self.Tick.UpdateTime[-2:] == '00':
            self.Buy(self.O[0], 1, '')
