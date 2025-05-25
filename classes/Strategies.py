from abc import ABC, abstractmethod 
import pandas as pd
from Trade import Trade
from utils.indicators import calculate_rsi_ema
from typing import Union
from Account import Account

class Strategy(ABC):
    @abstractmethod
    def signal(self, data: pd.DataFrame | pd.Series, *args, **kwargs):
        pass

    @abstractmethod
    def execute_strategy(self, trade: Trade,*args, **kwargs):
        pass

class RSI_Strategy(Strategy):
    def __init__(self, trade = None):
        super().__init__(trade)
        self.rsi_values = None

    def signal(self, data, *args, **kwargs):
        self.rsi_values = calculate_rsi_ema(data=data,
                                            period=14)
        
    def execute_strategy(self, trade: Trade, data: pd.DataFrame | pd.Series, account: Account, *args, **kwargs) -> Union[Trade, None]:
        for index, rsi_value in enumerate(self.rsi_values):
            # long position
            if rsi_value <= 30:
                pass
                # trade = Trade(symbol=kwargs.symbol,
                #               entry_price=data["Close"].iloc[index],
                #               account=account,
                #               shares=)