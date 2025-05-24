from abc import ABC, abstractmethod 
import pandas as pd
from Trade import Trade
from utils.indicators import calculate_rsi_ema

class Strategy(ABC):
    def __init__(self, trade: Trade = None):
        self.trade: Trade = trade

    @property
    def trade(self) -> Trade:
        return self.__trade
    
    @trade.setter
    def trade(self, trade: Trade) -> None:
        if not isinstance(trade, (Trade, None)):
            raise TypeError("Invalid trade object type")

        self.__trade = trade

    @abstractmethod
    def execute_strategy(self, *args, **kwargs):
        pass

class RSI_Strategy(Strategy):
    def __init__(self, trade = None):
        super().__init__(trade)
        self.rsi_values = None

    def execute_strategy(self, *args, **kwargs):
        if kwargs.data is None:
            raise ValueError("Missing data for using rsi strategy!")        
        
        if not isinstance(kwargs.data, (pd.DataFrame, pd.Series)):
            raise TypeError("Invalid data type")

        self.rsi_values = calculate_rsi_ema(kwargs.data)