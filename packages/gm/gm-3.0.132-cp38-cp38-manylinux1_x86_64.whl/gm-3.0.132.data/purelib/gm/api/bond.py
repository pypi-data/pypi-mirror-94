# coding=utf-8
from __future__ import unicode_literals, print_function, absolute_import

from typing import Text, List, Dict, Any

from gm.enum import OrderQualifier_Unknown
from gm.pb.account_pb2 import Order, OrderType_Limit, OrderBusiness_BOND_RRP
from .trade import _inner_place_order


def bond_reverse_repurchase_agreement(symbol, volume, price,
                                      order_type=OrderType_Limit,
                                      order_duration=OrderQualifier_Unknown,
                                      order_qualifier=OrderQualifier_Unknown,
                                      account_id=''
                                      ):
    # type: (Text, int, float, int, int, int, Text) -> List[Dict[Text, Any]]
    """
    国债逆回购
    :param symbol:                  标的
    :param volume:                  数量
    :param price:                   价格
    :param order_type:              委托类型
    :param order_duration:          委托时间属性
    :param order_qualifier:         委托成交属性
    :param account_id:              账户ID，不指定则使用默认账户
    :return:
    """
    o = Order()
    o.symbol = symbol
    o.volume = volume
    o.price = price
    o.order_type = order_type
    o.order_business = OrderBusiness_BOND_RRP
    o.order_qualifier = order_qualifier
    o.order_duration = order_duration
    o.account_id = account_id
    return _inner_place_order(o)
