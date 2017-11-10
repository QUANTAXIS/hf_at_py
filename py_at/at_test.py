#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
  Author:  HaiFeng --<galaxy>
  Purpose: main function
  Created: 2016/5/31
"""

import _thread
import sys
import os

import zmq  # netMQ
import gzip  # 解压
import json
from time import sleep  # 可能前面的import模块对time有影响,故放在最后

sys.path.append(os.path.join(sys.path[0], '..'))  # 调用父目录下的模块

from py_at.bar import Bar
from py_at.data import Data
from py_at.order_item import OrderItem
from py_at.adapters.ctp_trade import CtpTrade
from py_at.adapters.ctp_quote import CtpQuote
from py_at.enums import DirectType, OffsetType, OrderType
from py_at.structs import InfoField, OrderField, TradeField, ReqPackage
from py_at.tick import Tick


class at_test:
    """"""

    def __init__(self):
        """初始化 运行的目录下需要创建log目录"""

        """交易前置"""
        self.front_trade = ''
        # 行情前置
        self.front_quote = ''
        self.investor = ''
        self.pwd = ''
        self.broker = ''
        self.TradingDay = ''
        # self.log = open('orders.csv', 'w')
        # self.log.write('')  # 清空内容

        self.stra_instances = []

        self.q = CtpQuote()
        self.t = CtpTrade()

    def on_order(self, stra, order=OrderItem()):
        """此处调用ctp接口即可实现实际下单"""

        _order = order
        # self.log.write('{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\n'.format(len(p.Orders), stra.Bars[0].D, _order.Direction, _order.Offset, _order.Price, _order.Volume, _order.Remark))

        if stra.EnableOrder:
            print(order)
            # 平今与平昨;逻辑从C# 抄过来;没提示...不知道为啥,只能盲码了.
            if _order.Offset != OffsetType.Open:
                key = '{0}_{1}'.format(_order.Instrument, int(DirectType.Sell if _order.Direction == DirectType.Buy else DirectType.Buy))
                # 无效,没提示...pf = PositionField()
                pf = self.t.DicPositionField.get(key)
                if not pf or pf.Position <= 0:
                    print('没有对应的持仓')
                else:
                    volClose = min(pf.Position, _order.Volume)  # 可平量
                    instField = self.t.DicInstrument[_order.Instrument]
                    if instField.ExchangeID == 'SHFE':
                        tdClose = min(volClose, pf.TdPosition)
                        if tdClose > 0:
                            self.t.ReqOrderInsert(_order.Instrument, _order.Direction, OffsetType.CloseToday, _order.Price, tdClose, OrderType.Limit, 100)
                            volClose -= tdClose
                    if volClose > 0:
                        self.t.ReqOrderInsert(_order.Instrument, _order.Direction, OffsetType.Close, _order.Price, volClose, OrderType.Limit, 100)
            else:
                self.t.ReqOrderInsert(stra.Instrument, _order.Direction, OffsetType.Open, _order.Price, _order.Volume, OrderType.Limit, 100)

    def load_strategy(self):
        """加载../strategy目录下的策略"""
        """通过文件名取到对应的继承Data的类并实例"""
        # for path in ['strategies', 'private']:
        for path in ['strategies']:
            files = os.listdir(os.path.join(sys.path[0], '../strategies'))
            for f in files:
                if os.path.isdir(f) or os.path.splitext(f)[0] == '__init__' or os.path.splitext(f)[-1] != ".py":
                    continue
                # 目录结构???
                module_name = "{1}.{0}".format(os.path.splitext(f)[0], path)
                class_name = os.path.splitext(f)[0]

                module = __import__(module_name)  # import module

                c = getattr(getattr(module, class_name), class_name)  # 双层调用才是class,单层是为module

                if not issubclass(c, Data):  # 类c是Data的子类
                    continue
                print("# c:{0}", c)
                obj = Data()
                obj = c()  # new class
                print("# obj:{0}", obj)
                self.stra_instances.append(obj)

    def read_from_mq(self, stra):
        """netMQ"""
        _stra = Data()
        _stra = stra
        # pip install pyzmq即可安装
        context = zmq.Context()
        socket = context.socket(zmq.REQ)  # REQ模式,即REQ-RSP  CS结构
        # socket.connect('tcp://localhost:8888')	# 连接本地测试
        socket.connect('tcp://58.247.171.146:5055')  # 实际netMQ数据服务器地址
        # 请求数据格式
        req = ReqPackage()
        req.Type = 0  # BarType.Min ????
        req.Instrument = _stra.Instrument
        req.Begin = _stra.BeginDate
        req.End = _stra.EndDate
        # __dict__返回diction格式,即{key,value}格式
        p = req.__dict__
        socket.send_json(p)  # 直接发送__dict__转换的{}即可,不需要再转换成str

        # msg = socket.recv_unicode()	# 服务器此处查询出现异常, 排除中->C# 正常
        # 用recv接收,但是默认的socket中并没有此提示函数(可能是向下兼容的函数),不知能否转换为其他格式
        bs = socket.recv()  # 此处得到的是bytes

        # gzip解压:decompress(bytes)解压,会得到解压后的bytes,再用decode转成string
        gzipper = gzip.decompress(bs).decode()  # decode转换为string

        # json解析:与dumps对应,将str转换为{}
        bars = json.loads(gzipper)  # json解析

        # 此处对bars进行数据组合,即1min->nmin

        return bars

    def read_data_test(self):
        """取历史和实时K线数据,并执行策略回测"""
        stra = Data()
        for stra in self.stra_instances:
            stra.EnableOrder = False
            # 取数据
            ddoc = self.read_from_mq(stra)

            # print params os strategy
            # stra.OnOrder = self.on_order
            for p in stra.Params:
                print("{0}:{1}".format(p, stra.Params[p]), end=' ')

            for doc in ddoc:
                bar = Bar(doc["_id"], doc["High"], doc["Low"], doc["Open"], doc["Close"], doc["Volume"], doc["OpenInterest"])
                stra.__new_min_bar__(bar)  # 调Data的onbar
            stra.EnableOrder = True

        print("\ntest history is end.")

    def OnFrontConnected(self):
        """"""
        print("t:connected by client")
        self.t.ReqUserLogin(self.investor, self.pwd, self.broker)

    def relogin(self):
        """"""
        self.t.Release()
        print('sleep 60 seconds to wait try connect next time')
        sleep(60)
        self.t.ReqConnect(self.front_trade)

    def OnRspUserLogin(self, info=InfoField()):
        """"""

        print(info.ErrorID)
        if info.ErrorID == 7:
            _thread.start_new_thread(self.relogin, ())
        if info.ErrorID == 0:
            self.TradingDay = self.t.TradingDay
            if not self.q.IsLogin:
                self.q.OnFrontConnected = self.q_OnFrontConnected
                self.q.OnRspUserLogin = self.q_OnRspUserLogin
                self.q.OnRtnTick = self.q_Tick
                self.q.ReqConnect(self.front_quote)

    def OnOrder(self, order=OrderField):
        """"""
        print(order)

    def OnCancel(self, order=OrderField):
        """"""
        print(order)

    def OnTrade(self, trade=TradeField):
        """"""
        print(trade)

    def OnRtnErrOrder(self, order=OrderField, info=InfoField):
        """"""
        print(order)

    def q_OnFrontConnected(self):
        """"""
        print("q:connected by client")
        self.q.ReqUserLogin(self.broker, self.investor, self.pwd)

    def q_OnRspUserLogin(self, info=InfoField):
        """"""
        print(info)
        self.q.ReqSubscribeMarketData('rb1801')
        for stra in self.stra_instances:
            self.q.ReqSubscribeMarketData(stra.Instrument)

    def q_Tick(self, tick=Tick):
        """"""
        # print(tick)
        for data in self.stra_instances:
            if data.Instrument == tick.Instrument:
                data.on_tick(tick)
                for d2 in data.datalist:
                    if d2.Instrument == tick.Instrument:
                        d2.on_tick(tick)
                # print(tick)

    def CTPRun(self, front_trade='tcp://180.168.146.187:10000', front_quote='tcp://180.168.146.187:10010', broker='9999', investor='008109', pwd='1'):
        """"""
        self.t.OnFrontConnected = self.OnFrontConnected
        self.t.OnRspUserLogin = self.OnRspUserLogin
        self.t.OnRtnOrder = self.OnOrder
        self.t.OnRtnTrade = self.OnTrade
        self.t.OnRtnCancel = self.OnCancel
        self.t.OnRtnErrOrder = self.OnRtnErrOrder

        self.front_trade = front_trade
        self.front_quote = front_quote
        self.broker = broker
        self.investor = investor
        self.pwd = pwd
        self.t.ReqConnect(front_trade)


if __name__ == '__main__':
    p = at_test()
    if len(sys.argv) == 1:
        p.CTPRun()
    else:
        p.CTPRun(investor=sys.argv[1], pwd=sys.argv[2])
    p.load_strategy()
    # p.read_data_test()
    # 注销148行
    for stra in p.stra_instances:
        stra.SingleOrderOneBar = False
        stra.EnableOrder = True
        stra.OnOrder = p.on_order
    input()

