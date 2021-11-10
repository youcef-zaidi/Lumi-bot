from time import ctime

import model
import os
from dataclasses import dataclass

from binance.client import Client

from bot import TradeType, TradeData, OrderType


@dataclass
class API:
    api_key: str
    api_secret: str


class Controller:
    """Class that communicates with the view (frontend) and trading bot model"""

    # TODO implement methods communicating with the frontend (Django) and, in turn, with the model

    def __init__(self, trade_type: TradeType, order_type: OrderType, pair: tuple = ('BTC', 'USDT'), quantity=0.001, paper=True):
        self.api_key = os.environ.get('binance_api')
        self.api_secret = os.environ.get('binance_secret')
        self.api_data = API(self.api_key, self.api_secret)
        self.client = Client(self.api_data.api_key, self.api_data.api_secret)
        self.paper = paper
        if paper:
            self.client.API_URL = 'https://testnet.binance.vision/api'
        self.pair_str = pair[0] + pair[1]
        self.trade_data = TradeData(trade_type, order_type, pair, self.pair_str, quantity)
        self.model = model.Model(self.trade_data, self.client)

    def get_asset_balance(self, asset):
        return self.client.get_asset_balance(asset=asset)

    def create_order(self, symbol, side, order_type, quantity):  # might be redundant
        self.client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)

    def futures_account_transfer(self, asset, amount, f_type, timestamp=ctime()):
        self.client.futures_account_transfer(asset=asset, amount=amount, type=f_type, timestamp=timestamp)


controller = Controller(TradeType.SPOT, OrderType.MARKET, paper=True)
controller.model.bot.start()
