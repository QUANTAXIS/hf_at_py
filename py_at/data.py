#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2016/8/16'
"""

import time
import numpy as np

from py_at.enums import IntervalType, DirectType, OffsetType
from py_at.tick import Tick
from py_at.order_item import OrderItem
from py_at.bar import Bar
from py_at.switch import switch


class Data(object):
    '''数据类, 策略继承此类'''

    def __init__(self):
        '''初始所有变量'''
        '''K线序列'''
        self.Bars = []
        '''日线-日期'''
        self.DateD = []
        '''日线-开'''
        self.OpenD = []
        '''日线-高'''
        self.HighD = []
        '''日线-低'''
        self.LowD = []
        '''日线-收'''
        self.CloseD = []
        '''合约'''
        self.Instrument = ''
        '''周期'''
        self.Interval = 1
        '''周期类型'''
        self.IntervalType = IntervalType.Minute
        '''起始测试时间
        格式:yyyyMMdd[%Y%m%d]
        默认:20160101'''
        self.BeginDate = '20160101'
        '''结束测试时间
        格式:yyyyMMdd[%Y%m%d]
        默认:本地时间'''
        self.EndDate = time.strftime("%Y%m%d", time.localtime())  # 默认值取当日
        '''分笔数据
        Tick.Instrument用来判断是否有实盘数据'''
        self.Tick = Tick()
        '''参数'''
        self.Params = {}
        '''买卖信号'''
        self.Orders = []
        '''指标字典
        策略使用的指标保存在此字典中
        以便管理程序显示和处理'''
        self.IndexDict = {}
        '''策略标识'''
        self.ID = None
        '''允许委托下单'''
        self.EnableOrder = True
        '''每bar只执行一次交易'''
        self.SingleOrderOneBar = True

        # 序列变量
        self.inputs = {
            'date': np.array([]),
            'open': np.array([]),
            'high': np.array([]),
            'low': np.array([]),
            'close': np.array([]),
            'volume': np.array([]),
            'openinterest': np.array([]),
        }

        self._lastOrder = OrderItem()

        self.D = self.inputs['date']
        self.H = self.inputs['high']
        self.L = self.inputs['low']
        self.O = self.inputs['open']
        self.C = self.inputs['close']
        self.V = self.inputs['volume']
        self.I = self.inputs['openinterest']

    # 当前策略相关
    @property
    def AvgEntryPriceShort(self):
        '''开仓均价-空'''
        return self._lastOrder.AvgEntryPriceShort

    @property
    def AvgEntryPriceLong(self):
        '''开仓均价-多'''
        return self._lastOrder.AvgEntryPriceLong

    @property
    def PositionLong(self):
        '''持仓-多'''
        return self._lastOrder.PositionLong

    @property
    def PositionShort(self):
        '''持仓-空'''
        return self._lastOrder.PositionShort

    @property
    def EntryDateLong(self):
        '''开仓时间-多'''
        return self._lastOrder.EntryDateLong

    @property
    def EntryPriceLong(self):
        '''开仓价格-多'''
        return self._lastOrder.EntryPriceLong

    @property
    def ExitDateShort(self):
        '''平仓时间-空'''
        return self._lastOrder.ExitDateShort

    @property
    def ExitPriceShort(self):
        '''平仓价-空'''
        return self._lastOrder.ExitPriceShort

    @property
    def EntryDateShort(self):
        '''开仓时间-空'''
        return self._lastOrder.EntryDateShort

    @property
    def EntryPriceShort(self):
        '''开仓价-空'''
        return self._lastOrder.EntryPriceShort

    @property
    def ExitDateLong(self):
        '''平仓时间-多'''
        return self._lastOrder.ExitDateLong

    @property
    def ExitPriceLong(self):
        '''平仓价-多'''
        return self._lastOrder.ExitPriceLong

    @property
    def LastEntryDateShort(self):
        '''最后开仓时间-空'''
        return self._lastOrder.LastEntryDateShort

    @property
    def LastEntryPriceShort(self):
        '''最后开仓价-空'''
        return self._lastOrder.LastEntryPriceShort

    @property
    def LastEntryDateLong(self):
        '''最后开仓时间-多'''
        return self._lastOrder.LastEntryDateLong

    @property
    def LastEntryPriceLong(self):
        '''最后开仓价-多'''
        return self._lastOrder.LastEntryPriceLong

    @property
    def IndexEntryLong(self):
        '''开仓到当前K线数量-多'''
        return self._lastOrder.IndexEntryLong

    @property
    def IndexEntryShort(self):
        '''开仓到当前K线数量-空'''
        return self._lastOrder.IndexEntryShort

    @property
    def IndexLastEntryLong(self):
        '''最后平仓到当前K线数量-多'''
        return self._lastOrder.IndexLastEntryLong

    @property
    def IndexLastEntryShort(self):
        '''最后平仓到当前K线数量-空'''
        return self._lastOrder.IndexLastEntryShort

    @property
    def IndexExitLong(self):
        '''平仓到当前K线数量-多'''
        return self._lastOrder.IndexExitLong

    @property
    def IndexExitShort(self):
        '''平仓到当前K线数量-空'''
        return self._lastOrder.IndexExitShort

    @property
    def Position(self):
        '''持仓净头寸'''
        return self.PositionLong - self.PositionShort

    @property
    def CurrentBar(self):
        '''当前K线序号(0开始)'''
        return max(len(self.Bars) - 1, 0)

    def on_tick(self, tick):
        '''分笔数据处理'''
        self.Tick = tick
        # 取此tick对应的分钟时间
        # bar_time = time.strptime(time.strftime("%Y-%m-%d %H:%M", tick.UpdateTime), "%Y-%m-%d %H:%M")
        bar_time = tick.UpdateTime[:-2] + '00'  # time.strftime("%Y%m%d %H:%M:00", time.strptime(tick.UpdateTime, "%Y%m%d %H:%M:%S"))
        if len(self.Bars) == 0 or self.Bars[-1].D != bar_time:  # 新数据
            # bar_time, h, l, o, c, v, i, a)
            bar = Bar(bar_time, tick.LastPrice, tick.LastPrice, tick.LastPrice,
                      tick.LastPrice, tick.Volume, tick.OpenInterest)
            bar._pre_volume = tick.Volume

            self.__new_min_bar__(bar)  # 新K线数据插入
        else:
            bar = self.Bars[-1]
            bar.H = max(bar.H, tick.LastPrice)
            bar.L = min(bar.L, tick.LastPrice)
            bar.C = tick.LastPrice
            bar.V = tick.Volume - bar._pre_volume
            bar._pre_volume = tick.Volume
            bar.I = tick.OpenInterest
            bar.A = tick.AveragePrice

            self.__update_bar__(bar)

    def __new_min_bar__(self, bar):
        """有新min_bar添加"""

        bar_time = time.strptime(bar.D, "%Y%m%d %H:%M:%S")
        year = bar_time.tm_year
        mon = bar_time.tm_mon
        day = bar_time.tm_mday
        hour = bar_time.tm_hour
        mins = bar_time.tm_min
        for case in switch(self.IntervalType):
            if case(IntervalType.Minute):
                mins = bar_time.tm_min // self.Interval * self.Interval
                break
            if case(IntervalType.Hour):
                hour = hour // self.Interval
                mins = 0
                break
            if case(IntervalType.Day):
                hour = 0
                mins = 0
                break
            if case(IntervalType.Month):
                hour = 0
                mins = 0
                day = 1
                break
            if case(IntervalType.Year):
                hour = 0
                mins = 0
                day = 1
                mon = 1
                break
            if case(IntervalType.Week):
                hour = 0
                mins = 0
                # 用周号替换日期
                day = time.strftime('%W', bar_time)
                break

        bar_time = time.strptime('{0}-{1}-{2} {3}:{4}'.format(
            year, mon, day, hour, mins), '%Y-%m-%d %H:%M')
        # time -> str
        bar_time = time.strftime('%Y-%m-%d %H:%M:%S', bar_time)
        if len(self.Bars) == 0 or self.Bars[-1].D != bar_time:
            bar.D = bar_time
            self.Bars.append(bar)

            self.D = np.append(self.D, bar.D)
            self.H = np.append(self.H, bar.H)
            self.L = np.append(self.L, bar.L)
            self.O = np.append(self.O, bar.O)
            self.C = np.append(self.C, bar.C)
            self.V = np.append(self.V, bar.V)
            self.I = np.append(self.I, bar.I)
        else:
            old_bar = self.Bars[-1]
            self.H[-1] = old_bar.H = max(bar.H, old_bar.H)
            self.L[-1] = old_bar.L = min(bar.L, old_bar.L)
            self.C[-1] = old_bar.C = bar.C
            old_bar.V += bar.V
            self.V[-1] = old_bar.V
            self.I[-1] = old_bar.I = bar.I
            # bar.A = tick.AveragePrice
        # 日线数据处理
        date = '{0}-{1}-{2}'.format(year, mon, day)
        if len(self.DateD) == 0 or self.DateD[-1] != date:
            self.DateD.insert(0, date)
            self.OpenD.insert(0, bar.O)
            self.HighD.insert(0, bar.H)
            self.LowD.insert(0, bar.L)
            self.CloseD.insert(0, bar.C)
        else:
            self.HighD[-1] = max(self.HighD[-1], bar.H)
            self.LowD[-1] = min(self.LowD[-1], bar.L)
            self.CloseD[-1] = bar.C

        self.BarUpdate()

    def __update_bar__(self, bar):
        """更新当前数据序列"""

        self.D[-1] = bar.D
        self.H[-1] = bar.H
        self.L[-1] = bar.L
        self.O[-1] = bar.O
        self.C[-1] = bar.C
        self.V[-1] = bar.V
        self.I[-1] = bar.I

        self.HighD[-1] = max(self.HighD[-1], bar.H)
        self.LowD[-1] = min(self.LowD[-1], bar.L)
        self.CloseD[-1] = bar.C

        self.BarUpdate(bar)

    def BarUpdate(self, bar):
        """数据更新时调用此函数"""
        pass

    def OnOrder(self, stra, order):
        """继承类中实现此函数,有策略信号产生时调用"""
        pass

    def __order__(self, direction, offset, price, volume, remark):
        """策略执行信号"""

        if self.SingleOrderOneBar and (self.LastEntryDateLong == self.D[-1]
                                       or self.LastEntryDateShort == self.D[-1]
                                       or self.ExitDateLong == self.D[-1]
                                       or self.ExitDateShort == self.D[-1]):
            return
        order = OrderItem()
        order.Instrument = self.Instrument
        order.DateTime = self.D[-1]
        order.Direction = direction
        order.Offset = offset
        order.Price = price
        order.Volume = volume
        order.Remark = remark

        self.Orders.append(order)

        # 处理策略相关属性
        order.IndexEntryLong = self._lastOrder.IndexEntryLong
        order.IndexExitLong = self._lastOrder.IndexExitLong
        order.IndexEntryShort = self._lastOrder.IndexEntryShort
        order.IndexExitShort = self._lastOrder.IndexExitShort
        order.IndexLastEntryLong = self._lastOrder.IndexLastEntryLong
        order.IndexLastEntryShort = self._lastOrder.IndexLastEntryShort
        order.AvgEntryPriceLong = self._lastOrder.AvgEntryPriceLong
        order.AvgEntryPriceShort = self._lastOrder.AvgEntryPriceShort
        order.PositionLong = self._lastOrder.PositionLong
        order.PositionShort = self._lastOrder.PositionShort
        order.EntryDateLong = self._lastOrder.EntryDateLong
        order.EntryDateShort = self._lastOrder.EntryDateShort
        order.EntryPriceLong = self._lastOrder.EntryPriceLong
        order.EntryPriceShort = self._lastOrder.EntryPriceShort
        order.ExitDateLong = self._lastOrder.ExitDateLong
        order.ExitDateShort = self._lastOrder.ExitDateShort
        order.ExitPriceLong = self._lastOrder.ExitPriceLong
        order.ExitPriceShort = self._lastOrder.ExitPriceShort
        order.LastEntryDateLong = self._lastOrder.LastEntryDateLong
        order.LastEntryDateShort = self._lastOrder.LastEntryDateShort
        order.LastEntryPriceLong = self._lastOrder.LastEntryPriceLong
        order.LastEntryPriceShort = self._lastOrder.LastEntryPriceShort

        diroff = '{0}-{1}'.format(order.Direction.name, order.Offset.name)
        for case in switch(diroff):
            if case('Buy-Open'):
                order.PositionLong += order.Volume
                order.AvgEntryPriceLong = (
                    self._lastOrder.PositionLong * self._lastOrder.
                    AvgEntryPriceLong + order.Volume * order.Price) / (
                        self._lastOrder.Volume + order.Volume)
                if self._lastOrder.PositionLong == 0:
                    order.IndexEntryLong = len(self.Bars) - 1
                    order.EntryDateLong = self.D[-1]  # str '20160630 21:25:00'
                    order.EntryPriceLong = order.Price
                order.IndexLastEntryLong = len(self.Bars) - 1
                order.LastEntryPriceLong = order.Price
                order.LastEntryDateLong = self.D[-1]
                break

            if case('Buy-Close'):
                c_lots = min(self._lastOrder.PositionShort,
                             order.Volume)  # 能够平掉的数量
                if c_lots <= 0:  # 无仓可平
                    print('平仓量>持仓量')
                    break
                order.PositionShort -= c_lots

                order.IndexExitShort = len(self.Bars) - 1
                order.ExitDateShort = self.D[-1]
                order.ExitPriceShort = order.Price
                break

            if case('Sell-Open'):
                order.PositionShort += order.Volume
                order.AvgEntryPriceShort = (
                    self._lastOrder.PositionShort * self._lastOrder.
                    AvgEntryPriceShort + order.Volume * order.Price) / (
                        self._lastOrder.Volume + order.Volume)
                if self._lastOrder.PositionShort == 0:
                    order.IndexEntryShort = len(self.Bars) - 1
                    order.EntryDateShort = self.D[
                        -1]  # time or double or str ???
                    order.EntryPriceShort = order.Price
                order.IndexLastEntryShort = len(self.Bars) - 1
                order.LastEntryPriceShort = order.Price
                order.LastEntryDateShort = self.D[-1]
                break

            if case('Sell-Close'):
                c_lots = min(self._lastOrder.PositionLong,
                             order.Volume)  # 能够平掉的数量
                if c_lots <= 0:  # 无仓可平
                    print('平仓量>持仓量')
                    break
                order.PositionLong -= c_lots

                order.IndexExitLong = len(self.Bars) - 1
                order.ExitDateLong = self.D[-1]
                order.ExitPriceLong = order.Price
                break

        self._lastOrder = order

        self.OnOrder(self, order)

    def Buy(self, price, volume, remark):
        """买开"""
        self.__order__(DirectType.Buy, OffsetType.Open, price, volume, remark)

    def Sell(self, price, volume, remark):
        """买平"""
        self.__order__(DirectType.Sell, OffsetType.Close, price, volume,
                       remark)

    def SellShort(self, price, volume, remark):
        """卖开"""
        self.__order__(DirectType.Sell, OffsetType.Open, price, volume, remark)

    def BuyToCover(self, price, volume, remark):
        """买平"""
        self.__order__(DirectType.Buy, OffsetType.Close, price, volume, remark)
