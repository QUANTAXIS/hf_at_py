#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2017/10/30'
"""

from enum import Enum


class DirectType(Enum):
    """"""
    Buy = 0
    Sell = 1

    def __int__(self):
        return self.value


class OffsetType(Enum):
    """"""
    Open = 0
    Close = 1
    CloseToday = 2

    # ----------------------------------------------------------------------
    def __int__(self):
        return self.value


class OrderType(Enum):
    """"""
    Limit = 0
    Market = 1
    FAK = 2
    FOK = 3

    def __int__(self):
        return self.value


class OrderStatus(Enum):
    """"""
    Normal = 0
    Partial = 1
    Filled = 2
    Canceled = 3
    Error = 4

    def __int__(self):
        return self.value


class IntervalType(Enum):
    """时间类型:秒,分,时,日,周,月,年"""

    Second = 0
    Minute = 1
    Hour = 2
    Day = 3
    Week = 4
    Month = 5
    Year = 6

    def __int__(self):
        """return int value"""
        return self.value


class BarType(Enum):
    """"""
    Min = 0
    Day = 1
    Real = 2
    Time = 3
    Product = 4
    TradeDate = 5

    def __int__(self):
        """return int value"""
        return self.value
