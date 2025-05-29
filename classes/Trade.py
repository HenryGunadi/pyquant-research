from __future__ import annotations
import uuid
from datetime import date, datetime
from abc import ABC, abstractmethod
from typing import Literal

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .Account import Account

class ExitCondition(ABC):
    def __init__(self, expiration: datetime = None):
        self.expiration = expiration

    def is_expired(self, current_time: datetime) -> bool:
        if self.expiration is None:
            return False
        return current_time >= self.expiration

    @abstractmethod
    def should_exit(self, current_price, current_time: datetime) -> bool:
        pass

class StopLossExit(ExitCondition):
    def __init__(self, stop_price: float, expiration: datetime = None):
        super().__init__(expiration)
        self.stop_price = stop_price

    def should_exit(self, current_price, current_time: datetime) -> bool:
        if self.is_expired(current_time):
            return False
        return current_price <= self.stop_price
    
class Exit(ExitCondition):
    def __init__(self, exit_price: float, expiration: datetime = None):
        super().__init__(expiration)
        self.exit_price = exit_price

    def should_exit(self, current_price, current_time: datetime) -> bool:
        if self.is_expired(current_time):
            return False
        return current_price >= self.exit_price

class Trade():
    def __init__(self, symbol: str, entry_time: datetime, entry_price: float, account: "Account", shares: int, position_type: Literal["long", "short"], stop_loss: StopLossExit = None, exit: Exit = None):
        self._id: str = str(uuid.uuid4())
        self.symbol: str = symbol
        # assume these are non fractional shares
        self.shares: int = shares
        self._entry_price: float = entry_price
        self.entry_time: datetime = entry_time
        self.stop_loss: StopLossExit = stop_loss
        self.exit: Exit = exit
        self.account: "Account" = account
        self._average_price: float = entry_price
        self._invested: float = shares * entry_price
        self.position_type = position_type
        self._pnl: float = 0
        self.exit_time: datetime = None
        
        self.account.portfolio.add_trade(self)

    @property
    def id(self) -> str:
        return self._id
    
    @property
    def pnl(self) -> float:
        return self._pnl
    
    @property
    def shares(self) -> int:
        return self._shares

    @property
    def account(self) -> "Account":
        return self._account

    @property
    def entry_price(self) -> float:
        return self._entry_price
    
    @property 
    def stop_loss(self) -> StopLossExit:
        return self._stop_loss
    
    @property 
    def exit(self) -> Exit:
        return self._exit
    
    @property
    def average_price(self) -> float:
        return self._average_price

    @property
    def invested(self) -> float:
        return self._invested
    
    @property
    def pnl_percentage(self) -> float:
        if self._invested == 0:
            return 0
        return (self._pnl / self._invested) * 100
    
    @stop_loss.setter
    def stop_loss(self, stop_loss: StopLossExit) -> None:
        # if not isinstance(stop_loss, (StopLossExit, type(None))):
        #     raise TypeError("Invalid stop loss object type")

        self._stop_loss = stop_loss

    @exit.setter
    def exit(self, exit: Exit) -> None:
        # if not isinstance(exit, (Exit, type(None))):
        #     raise TypeError("Invalid exit object type")

        self._exit = exit
    
    @account.setter
    def account(self, account: "Account") -> None:
        from .Account import Account
        
        if not isinstance(account, Account):
            raise TypeError("Invalid account type object")

        self._account = account
            
    @shares.setter
    def shares(self, shares: int) -> None:
        if shares <= 0:
            raise ValueError("Shares cannot be equal or less than zero")

        self._shares = shares

    def update_pnl(self, current_price: float):
        if self.position_type == "long":
            self._pnl = (current_price - self._average_price) * self.shares
        else:
            self._pnl = (self._average_price - current_price) * self.shares

    def increase_share(self, shares: int, price: float) -> None:
        if shares <= 0:
            raise ValueError("Shares cannot be equal or less than zero")
        self._account.can_execute_trade()
        total_cost = self._average_price * self._shares + price * shares
        self._shares += shares
        self._average_price = total_cost / self._shares
        self._invested = self._average_price * self._shares

    def close(self, exit_time: datetime):
        self.exit_time = exit_time
        self.account.portfolio.close_trade(trade=self)
        
    def __str__(self) -> str:
        return (
            f"Trade({self.id}): {self.symbol.upper()}\n"
            f"Position: {self.position_type} | Shares: {self.shares}\n"
            f"Entry: {self.entry_price:.2f} at {self.entry_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"Exit: {self.exit_time.strftime('%Y-%m-%d %H:%M:%S') if self.exit_time else 'OPEN'}\n"
            f"PnL: {self.pnl:.2f} ({self.pnl_percentage:.2f}%)"
        )
