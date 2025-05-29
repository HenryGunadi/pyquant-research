from __future__ import annotations
from abc import ABC, abstractmethod 
import pandas as pd
from utils.indicators import calculate_rsi_ema
from typing import Union, Literal
from dataclasses import dataclass

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Trade import Trade
    from .Account import Account

@dataclass
class Signal:
    position_type: str | None
    index: int | None
    rsi_value: float | None

class Strategy(ABC):
    @abstractmethod
    def next():
        pass

    @abstractmethod
    def signal(self, data: pd.DataFrame | pd.Series) -> str:
        pass

    @abstractmethod
    def execute_strategy(self, data: pd.DataFrame, account: Account, type: Literal["long", "short"], index, trade: "Trade"):
        pass

class RSI_Strategy(Strategy):
    rsi_values = [] 

    @staticmethod
    def signal(data: pd.DataFrame | pd.Series):
        RSI_Strategy.rsi_values = calculate_rsi_ema(data=data,
                                            period=14)

        for index, rsi_value in RSI_Strategy.rsi_values.items():
            if rsi_value <= 30:
                return Signal(position_type="long", index=index, rsi_value=RSI_Strategy.rsi_values[index])
            elif rsi_value >= 70:
                return Signal(position_type="short", index=index, rsi_value=RSI_Strategy.rsi_values[index])

        return Signal(position_type=None, index=None, rsi_value=None)

    @staticmethod
    def execute_strategy(data: pd.DataFrame | pd.Series, account: Account, index, trade: "Trade", position_type: Literal["long", "short"]) -> Union["Trade", None]:
        if index > len(data):
            print("Im returning")
            return
        
        print("INDEX : ", index)        
        if trade.exit.should_exit(current_price=data["High"].iloc[index] if position_type == "long" else data["Low"].iloc[index], current_time=data.iloc[index].index):
            trade.update_pnl(data["high"].iloc[index])
            trade.close(exit_time=data.index[index])
            return
        elif trade.stop_loss.should_exit(current_price=data["Low"].iloc[index] if position_type == "long" else data["High"].iloc[index], current_time=data.iloc[index].index):
            trade.update_pnl(data["Low"].iloc[index])
            trade.close(exit_time=data.index[index])
            return
        
        trade.update_pnl(data["Close"].iloc[index])
        
        RSI_Strategy.execute_strategy(data=data,
                                      account=account,
                                      index=index + 1,
                                      trade=trade,
                                      position_type=position_type)
        
    def next():
        pass