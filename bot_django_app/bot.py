import asyncio
from asyncio.tasks import sleep
import datetime
import threading
from multiprocessing import Process
import multiprocessing as mp
from dataclasses import dataclass
from enum import Enum

from binance.client import Client

import btalib
import pandas as pd


class TradeType(Enum):
    SPOT = 'SPOT'
    FUTURE = 'FUTURE'


class OrderType(Enum):
    MARKET = 1
    LIMIT = 2


class Sentiment(Enum):
    BEARISH = 1
    BULLISH = 2


@dataclass
class TradeData:
    trade_type: TradeType
    order_type: OrderType
    pair: tuple
    pair_str: str  # Trading pair (e.g. BTCUSDT)
    quantity: float


class Bot:
    """Class responsible for the implementation of the trading bot"""

    def __init__(self, api):
        self.api = api
        self.trade_data = None
        self.df = pd.DataFrame()
        self.stopped = False
        self.loop = asyncio.get_event_loop()
        self.orders = []
        self.fibo_lvls = []
        self.sentiment = None

    def set_trade_data(self, trade_data):
        self.trade_data = trade_data
        self.api.set_pair(trade_data.pair_str)

    def stop(self):
        self.stopped = True
        self.loop.stop()
        self.loop.close()

    def start(self):
        try:
            asyncio.ensure_future(self.populate_df(), loop=self.loop)
            asyncio.ensure_future(self.refresh_sentiment_from_fibo(), loop=self.loop)
            asyncio.ensure_future(self.start_trade(), loop=self.loop)
            self.loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            print(f'{datetime.datetime.now()} \t Closing Loop')
            self.stop()

    async def start_trade(self):
        await asyncio.sleep(60)
        print(f'{datetime.datetime.now()} \t Starting the trading\n')

        while not self.stopped:

            if len(self.orders) > 0:
                print(f'{datetime.datetime.now()} \t Attempting to close position with a profit/loss threshold')
                self.threshold_sell(profit_threshold=0.01, loss_threshold=-0.1)

            if self.get_rsi(timeframe=Client.KLINE_INTERVAL_1MINUTE) < 15 or self.get_rsi(
                    timeframe=Client.KLINE_INTERVAL_15MINUTE) < 15:
                print(f'{datetime.datetime.now()} \t 1m-15m RSI is very low, strong buy signal')
                self.__buy(self.trade_data.quantity)
            if self.get_rsi(timeframe=Client.KLINE_INTERVAL_30MINUTE) < 25 or self.get_rsi(
                    timeframe=Client.KLINE_INTERVAL_1HOUR) < 25:
                print(f'{datetime.datetime.now()} \t 30m-60m RSI is low, buy signal, but the trend is being checked too')
                self.trendfollow_buy()
            if self.get_rsi(timeframe=Client.KLINE_INTERVAL_30MINUTE) < 35 and self.get_rsi(
                    timeframe=Client.KLINE_INTERVAL_1HOUR) < 50:
                if self.get_ema(timeframe=Client.KLINE_INTERVAL_5MINUTE) or self.get_ema(
                        timeframe=Client.KLINE_INTERVAL_30MINUTE) > self.df.iloc[-1].Price:
                    print(f'{datetime.datetime.now()} \t 30m-60m RSI is neutral, but ema is higher than current price, buy signal')
                    self.__buy(self.trade_data.quantity)
            if self.get_sma(timeframe=Client.KLINE_INTERVAL_1HOUR) > (
                    self.df.iloc[-1].Price + self.df.iloc[-1].Price * (1 / 4)):
                print(f'{datetime.datetime.now()} \t RSI is high, but sma is much higher than current price, buy signal, but the trend is being '
                      'checked too')
                self.trendfollow_buy()

            if self.get_rsi(timeframe=Client.KLINE_INTERVAL_1MINUTE) > 85 or self.get_rsi(
                    timeframe=Client.KLINE_INTERVAL_15MINUTE) > 85:
                print(f'{datetime.datetime.now()} \t 1m-15m RSI is very high, strong sell signal')
                self.__sell(self.trade_data.quantity)
            if self.get_rsi(timeframe=Client.KLINE_INTERVAL_30MINUTE) > 65 or self.get_rsi(
                    timeframe=Client.KLINE_INTERVAL_1HOUR) > 50:
                if self.get_ema(timeframe=Client.KLINE_INTERVAL_30MINUTE) or self.get_ema(
                        timeframe=Client.KLINE_INTERVAL_1HOUR) < self.df.iloc[-1].Price:
                    print(f'{datetime.datetime.now()} \t 30m-60m RSI is neutral, but ema is lower than current price, sell signal')
                    self.__sell(self.trade_data.quantity)
            if self.get_sma(timeframe=Client.KLINE_INTERVAL_1HOUR) + (
                    self.get_sma(timeframe=Client.KLINE_INTERVAL_1HOUR) * (1 / 4)) < self.df.iloc[-1].Price:
                print(f'{datetime.datetime.now()} \t RSI is low, but sma is much lower than current price, sell signal')
                self.__sell(self.trade_data.quantity)

            if self.sentiment == Sentiment.BEARISH:
                if any(lvl < self.df.iloc[-1].Price for lvl in self.fibo_lvls[-3:]):
                    self.__sell(self.trade_data.quantity)
            else:
                if all(lvl > self.df.iloc[-1].Price for lvl in self.fibo_lvls[-3:]):
                    self.__buy(self.trade_data.quantity)
            await asyncio.sleep(5)

    async def populate_df(self):
        print(f'\n\n{datetime.datetime.now()} \t Gathering Data for provided coin pair ' + self.trade_data.pair_str)

        while not self.stopped:
            await asyncio.sleep(3)
            realtime_data = await self.api.get_data()
            print(f'\n{realtime_data}\n')
            self.df = self.df.append(realtime_data, ignore_index=True)
            if len(self.df) > 10000:
                self.df = self.df.iloc[len(self.df) - 10000:]

    def __buy(self, quantity):
        if len(self.orders) < 3 or not all(order['side'] == 'BUY' for order in self.orders[-3:]):
            if float(self.api.client.get_asset_balance(self.trade_data.pair[0])['free']) >= quantity:
                order = self.api.client.create_order(symbol=self.trade_data.pair_str, side='BUY', type='MARKET',
                                                     quantity=quantity)
                self.orders.append(order)
                print(f'{datetime.datetime.now()} \t Buy request created')
            else:
                print(f'{datetime.datetime.now()} \t Not enough capital to execute trade')

    def __sell(self, quantity):
        if len(self.orders) < 3 or not all(order['side'] == 'SELL' for order in self.orders[-3:]):
            if float(self.api.client.get_asset_balance(self.trade_data.pair[0])['free']) >= quantity:
                order = self.api.client.create_order(symbol=self.trade_data.pair_str, side='SELL', type='MARKET',
                                                     quantity=quantity)
                self.orders.append(order)
                print(f'{datetime.datetime.now()} \t Sell request created')
                return True
            else:
                print(f'{datetime.datetime.now()} \t Not enough capital to execute trade')
        return False

    def __close_position(self, quantity):
        self.api.client.create_order(symbol=self.trade_data.pair_str, side='SELL', type='MARKET',
                                             quantity=quantity)
        print(f'{datetime.datetime.now()} \t Sell request created')

    def trendfollow_buy(self):
        lookback_period = self.df.iloc[-10:]
        cumul_ret = (lookback_period.Price.pct_change() + 1).cumprod() - 1
        if abs(cumul_ret[cumul_ret.last_valid_index()]) > 0.003:
            self.__buy(self.trade_data.quantity)
        else:
            print(f'{datetime.datetime.now()} \t No trendfollow buy')

    def threshold_sell(self, profit_threshold, loss_threshold):
        if len(self.orders) > 0:
            order = self.orders[-1]
            pct_change_ret = (100 * (float(self.df.iloc[-1].Price) - float(order['fills'][0]['price']))) / float(
                order['fills'][0]['price'])
            if order['side'] == 'BUY':
                if pct_change_ret > profit_threshold or pct_change_ret < loss_threshold:
                    print(f'{datetime.datetime.now()} \t Closing buy position with a return of: ' + str(pct_change_ret) + '%')
                    success = self.__sell(self.trade_data.quantity)
                    if success:
                        print(f'{datetime.datetime.now()} \t Sell successful')
                        self.orders.remove(order)
                    else:
                        print(f'{datetime.datetime.now()} \t Sell unsuccessful')
                else:
                    print(f'{datetime.datetime.now()} \t No sell')
            else:
                if -pct_change_ret > profit_threshold or -pct_change_ret < loss_threshold:
                    print(f'{datetime.datetime.now()} \t Closing sell position with a return of: ' + str(-pct_change_ret) + '%')
                    self.__close_position(self.trade_data.quantity)
                    self.orders.remove(order)

    def get_dataframe(self, timeframe=Client.KLINE_INTERVAL_1HOUR):
        timestamp = self.api.client._get_earliest_valid_timestamp(self.trade_data.pair_str,
                                                                  Client.KLINE_INTERVAL_1MONTH)
        klines = self.api.client.get_historical_klines(self.trade_data.pair_str, timeframe, timestamp, limit=1000)
        df = pd.DataFrame(klines)
        df = df.iloc[:, :6]
        df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index, unit='ms')
        df = df.astype(float)
        return df

    def get_sma(self, timeframe, period=20):
        df = self.get_dataframe(timeframe=timeframe)
        print(f'{datetime.datetime.now()} \t sma ' + str(df.Close.tail(period).mean()))
        return df.Close.tail(period).mean()

    def get_ema(self, timeframe, period=20):
        df = self.get_dataframe(timeframe=timeframe)
        ema = btalib.ema(df, period=period)
        print(f'{datetime.datetime.now()} \t ema: ' + str(timeframe) + ' ' + str(ema.df.ema[-1]))
        return ema.df.ema[-1]

    def get_rsi(self, timeframe, period=14):
        df = self.get_dataframe(timeframe=timeframe)
        if period > len(df) - 1:
            period = len(df) - 1
        rsi = btalib.rsi(df, period=period)
        print(f'{datetime.datetime.now()} \t rsi: ' + str(timeframe) + ' ' + str(rsi.df.rsi[-1]))
        return rsi.df.rsi[-1]

    def __get_highest_and_lowest_swing(self):
        highest_swing = -1
        lowest_swing = -1
        df = self.get_dataframe(timeframe=Client.KLINE_INTERVAL_15MINUTE)
        for i in range(1, df.shape[0] - 1):
            if df['High'][i] > df['High'][i - 1] and df['High'][i] > df['High'][i + 1] and (
                    highest_swing == -1 or (
                    df['High'][highest_swing] < df['High'][i] < df['High'][highest_swing] * 1.05)):
                highest_swing = i
            if df['Low'][i] < df['Low'][i - 1] and df['Low'][i] < df['Low'][i + 1] and (
                    lowest_swing == -1 or (df['Low'][lowest_swing] * 0.95 < df['Low'][i] < df['Low'][lowest_swing])):
                lowest_swing = i
        return highest_swing, lowest_swing

    def __get_max_and_min_lvl(self):
        hi, lo = self.__get_highest_and_lowest_swing()
        df = self.get_dataframe(timeframe=Client.KLINE_INTERVAL_15MINUTE)
        max_level = df['High'][hi]
        min_level = df['Low'][lo]
        return max_level, min_level

    def get_fibonacci_ratio_lvls(self):
        max_level, min_level = self.__get_max_and_min_lvl()
        highest_swing, lowest_swing = self.__get_highest_and_lowest_swing()
        ratios = [0, 0.236, 0.382, 0.618, 0.786, 1]
        levels = []
        for ratio in ratios:
            if highest_swing > lowest_swing:  # Uptrend
                levels.append(max_level - (max_level - min_level) * ratio)
            else:  # Downtrend
                levels.append(min_level + (max_level - min_level) * ratio)
        return levels

    async def refresh_sentiment_from_fibo(self):
        while not self.stopped:
            self.fibo_lvls = self.get_fibonacci_ratio_lvls()
            if self.fibo_lvls[0] > self.fibo_lvls[-1]:
                self.sentiment = Sentiment.BEARISH
            else:
                self.sentiment = Sentiment.BULLISH
            await asyncio.sleep(900)
