# !/usr/bin/python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2017/11/16'
"""

from py_at.strategy import Strategy
from py_at.enums import IntervalType
from py_at.structs import OrderField, TradeField, InfoField
from py_at.data import Data
from py_at.tick import Tick
from py_at.bar import Bar


class Test(Strategy):
    ''''''

    def __init__(self, jsonfile=''):
        super().__init__(jsonfile)
        data = self.Datas[0]
        data.Instrument = 'rb1805'
        data.Interval = 1
        data.IntervalType = IntervalType.Minute
        self.BeginDate = '20171111'
        self.ordered = False

    def OnBarUpdate(self, data=Data, bar=Bar):
        if self.Tick.Instrument == '':
            return
        print(self.Datas[0].Tick.UpdateTime[-2:])
        if self.Tick.UpdateTime[-2:] == '00' or self.Tick.UpdateTime[-2:] == '30':
            if self.ordered:
                self.ordered = False
            else:
                self.ordered = True
                self.Buy(self.O[0], 1, '')

    def OnOrder(self, order=OrderField()):
        """委托响应"""
        print('strategy order')
        print(order)

    def OnTrade(self, trade=TradeField()):
        """成交响应"""
        print('strategy trade')
        print(trade)

    def OnCancel(self, order):
        """撤单响应"""
        print('strategy cancel')
        print(order)

    def OnErrOrder(self, order=OrderField(), info=InfoField()):
        """委托错误"""
        print('strategy err order')
        print(order)

    def OnErrCancel(self, order=OrderField(), info=InfoField()):
        """撤单错误"""
        print('strategy err cancel')
        print(order)
