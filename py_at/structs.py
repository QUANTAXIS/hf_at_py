#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = ''
__author__ = 'HaiFeng'
__mtime__ = '2016/9/21'
"""

from py_at.enums import DirectType, OffsetType, OrderStatus


class ReqPackage:
    """数据请求格式包"""

    def __init__(self):
        """Constructor"""

        self.Type = 0
        self.Instrument = ''
        self.Begin = ''
        self.End = ''


class InfoField:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.ErrorID = 0
        self.ErrorMsg = '正确'

    def __str__(self):
        # return 'ErrorID:{0}, ErrorMsg:{1}'.format(self.ErrorID, self.ErrorMsg)
        return '{{"ErrorID":{self.ErrorID}, "ErrorMsg":"{self.ErrorMsg}"}}'.format(
            self=self)

    @property
    def __dict__(self):
        return {'ErrorID': self.ErrorID, 'ErrorMsg': self.ErrorMsg}


########################################################################
class OrderField:
    """报单响应"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """initionalize"""

        self.OrderID = ""
        self.InstrumentID = ""
        self.Direction = DirectType.Buy
        self.Offset = OffsetType.Open
        self.LimitPrice = 0.0
        self.AvgPrice = 0.0
        self.InsertTime = ""
        self.TradeTime = ""
        self.TradeVolume = 0
        self.Volume = 0
        self.VolumeLeft = 0
        self.Status = OrderStatus.Normal
        self.StatusMsg = ""
        self.IsLocal = False
        self.Custom = 0
        self.SysID = ""

    # ----------------------------------------------------------------------
    def __str__(self):
        """"""
        return '{self.OrderID}, {self.InstrumentID}, {self.Direction}, {self.Offset}, {self.LimitPrice}, {self.AvgPrice}, {self.InsertTime}, {self.TradeTime}, {self.TradeVolume}, {self.Volume}, {self.VolumeLeft}, {self.Status}, {self.StatusMsg}, {self.IsLocal}, {self.Custom}, {self.SysID}'.format(
            self=self)

    @property
    def __dict__(self):  # 如何控制dict的字段次序?:交由客户端处理
        return {
            'OrderID': self.OrderID,
            'InstrumentID': self.InstrumentID,
            'Direction': self.Direction.name,
            'Offset': self.Offset.name,
            'LimitPrice': self.LimitPrice,
            'AvgPrice': self.AvgPrice,
            'InsertTime': self.InsertTime,
            'TradeTime': self.TradeTime,
            'TradeVolume': self.TradeVolume,
            'Volume': self.Volume,
            'VolumeLeft': self.VolumeLeft,
            'Status': self.Status.name,
            'StatusMsg': self.StatusMsg,
            'IsLocal': self.IsLocal,
            'Custom': self.Custom,
            'SysID': self.SysID
        }


########################################################################
class TradeField:
    """成交响应"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        self.TradeID = ''
        self.InstrumentID = ''
        self.ExchangeID = ''
        self.Direction = DirectType.Buy
        self.Offset = OffsetType.Open
        self.Price = 0.0
        self.Volume = 0
        self.TradeTime = ''
        self.TradingDay = ''
        self.OrderID = ''
        self.SysID = ''

    # ----------------------------------------------------------------------
    def __str__(self):
        """"""
        return '{self.TradeID}, {self.InstrumentID}, {self.ExchangeID}, {self.Direction}, {self.Offset}, {self.Price}, {self.Volume}, {self.TradeTime}, {self.TradingDay}, {self.OrderID}, {self.SysID}'.format(
            self=self)

    @property
    def __dict__(self):
        return {
            'TradeID': self.TradeID,
            'InstrumentID': self.InstrumentID,
            'ExchangeID': self.ExchangeID,
            'Direction': self.Direction.name,
            'Offset': self.Offset.name,
            'Price': self.Price,
            'Volume': self.Volume,
            'TradeTime': self.TradeTime,
            'TradingDay': self.TradingDay,
            'OrderID': self.OrderID,
            'SysID': self.SysID
        }


########################################################################
class InstrumentField:
    """合约"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        self.InstrumentID = ''
        self.ProductID = ''
        self.ExchangeID = ''
        self.VolumeMultiple = ''
        self.PriceTick = 0.0
        self.MaxOrderVolume = 9999

    # ----------------------------------------------------------------------
    def __str__(self):
        """"""
        return '{self.InstrumentID}, {self.ProductID}, {self.ExchangeID}, {self.VolumeMultiple}, {self.PriceTick}, {self.MaxOrderVolume}'.format(
            self=self)

    @property
    def __dict__(self):
        return {
            'InstrumentID': self.InstrumentID,
            'ProductID': self.ProductID,
            'ExchangeID': self.ExchangeID,
            'VolumeMultiple': self.VolumeMultiple,
            'PriceTick': self.PriceTick,
            'MaxOrderVolume': self.MaxOrderVolume
        }


########################################################################
class TradingAccount:
    """交易帐户"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        self.PreBalance = 0.0
        self.PositionProfit = 0.0
        self.CloseProfit = 0.0
        self.Commission = 0.0
        self.CurrMargin = 0.0
        self.FrozenCash = 0.0
        self.Available = 0.0
        self.Fund = 0.0
        self.Risk = 0.0

    # ----------------------------------------------------------------------
    def __str__(self):
        """"""
        return '{self.PreBalance}, {self.PositionProfit}, {self.CloseProfit}, {self.Commission}, {self.CurrMargin}, {self.FrozenCash}, {self.Available}, {self.Fund}, {self.Risk}'.format(
            self=self)

    @property
    def __dict__(self):
        return {
            'PreBalance': self.PreBalance,
            'PositionProfit': self.PositionProfit,
            'CloseProfit': self.CloseProfit,
            'Commission': self.Commission,
            'CurrMargin': self.CurrMargin,
            'FrozenCash': self.FrozenCash,
            'Available': self.Available,
            'Fund': self.Fund,
            'Risk': self.Risk
        }


########################################################################
class PositionField:
    """持仓"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""

        self.InstrumentID = ''
        self.Direction = DirectType.Buy
        self.Price = 0.0
        self.Position = 1
        self.YdPosition = 0
        self.TdPosition = 0
        self.CloseProfit = 0.0
        self.PositionProfit = 0.0
        self.Commission = 0.0
        self.Margin = 0.0

    # ----------------------------------------------------------------------
    def __str__(self):
        """"""
        return (
            '{self.InstrumentID}, {self.Direction}, {self.Price}, {self.Position}, {self.TdPosition}, {self.YdPosition}, {self.CloseProfit}, {self.PositionProfit}, {self.Commission}, {self.Margin}'
        ).format(self=self)

    @property
    def __dict__(self):
        return {
            'InstrumentID': self.InstrumentID,
            'Direction': self.Direction.name,
            'Price': self.Price,
            'Position': self.Position,
            'TdPosition': self.TdPosition,
            'YdPosition': self.YdPosition,
            'CloseProfit': self.CloseProfit,
            'PositionProfit': self.PositionProfit,
            'Commission': self.Commission,
            'Margin': self.Margin
        }
