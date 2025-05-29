from typing import List
from .Trade import Trade
import datetime

class Portfolio():
    def __init__(self):
        self.__active_trades: List[Trade] = []
        self.__closed_trades: List[Trade] = []
        
    @property
    def active_trades(self) -> List[Trade]:
        return self.__active_trades
    
    @property
    def closed_trades(self) -> List[Trade]:
        return self.__closed_trades

    def add_trade(self, trade: Trade):
        self.active_trades.append(trade)

    def close_trade(self, trade: Trade):
        self.active_trades.remove(trade)
        self.closed_trades.append(trade)