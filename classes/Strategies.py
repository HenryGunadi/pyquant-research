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
                return Signal(position_type="long", index=index)
            elif rsi_value >= 70:
                return Signal(position_type="short", index=index)

        return Signal(position_type=None, index=None)

    @staticmethod
    def execute_strategy(data: pd.DataFrame | pd.Series, account: Account, index, trade: "Trade") -> Union["Trade", None]:
        print("Current index : ", index + 1)
        if trade.exit.should_exit(data["High"].iloc[index + 1], index + 1):
            trade.update_pnl(data["high"].iloc[index + 1])
            trade.close()
            return
        elif trade.stop_loss.should_exit(data["Low"].iloc[index + 1], index + 1):
            trade.update_pnl(data["Low"].iloc[index + 1])
            trade.close()
            return
        
        trade.update_pnl(data["Close"].iloc[index + 1], index + 1)
        RSI_Strategy.execute_strategy(data, account, index=index + 1)

    def next():
        pass