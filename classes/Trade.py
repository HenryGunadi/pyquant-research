import uuid
from Account import Account
from datetime import date, datetime
from abc import ABC, abstractmethod
from Strategies import Strategy
from typing import Literal

class ExitCondition(ABC):
    def __init__(self, expiration: datetime = None):
        self.expiration = expiration

    def is_expired(self, current_time: datetime) -> bool:
        if self.expiration is None:
            return False
        return current_time >= self.expiration

    @abstractmethod
    def should_exit(self, trade, current_price, current_time: datetime) -> bool:
        pass

class StopLossExit(ExitCondition):
    def __init__(self, stop_price: float, expiration: datetime = None):
        super().__init__(expiration)
        self.stop_price = stop_price

    def should_exit(self, trade, current_price, current_time: datetime) -> bool:
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
    def __init__(self, symbol: str, entry_time: datetime, entry_price: float, account: Account, shares: int, position_type: Literal["long", "short"], strategy: Strategy = None, stop_loss: StopLossExit = None, exit: Exit = None):
        self.__id: str = str(uuid.uuid4())
        self.symbol: str = symbol
        # assume these are non fractional shares
        self.shares: int = shares
        self.__entry_price: float = entry_price
        self.__entry_time: datetime = entry_time
        self.stop_loss: StopLossExit = stop_loss
        self.exit: Exit = exit
        self.account: Account = account
        self.__average_price: float = entry_price
        self.__invested: float = shares * entry_price
        self.strategy: Strategy = strategy
        self.position_type = position_type
        self.__pnl: float = 0

    @property
    def id(self) -> str:
        return self.__id
    
    @property
    def pnl(self) -> float:
        return self.__pnl
    
    @property
    def entry_time(self) -> datetime:
        return self.__entry_time
    
    @property
    def shares(self) -> int:
        return self.__shares

    @property
    def account(self) -> Account:
        return self.__account

    @property
    def entry_price(self) -> float:
        return self.__entry_price
    
    @property 
    def stop_loss(self) -> StopLossExit:
        return self.__stop_loss
    
    @property 
    def exit(self) -> Exit:
        return self.__exit
    
    @property
    def average_price(self) -> float:
        return self.__average_price

    @property
    def strategy(self) -> Strategy:
        return self.__strategy
    
    @property
    def invested(self) -> float:
        return self.__invested
    
    @property
    def pnl_percentage(self) -> float:
        if self.__invested == 0:
            return 0
        return (self.__pnl / self.__invested) * 100
    
    @strategy.setter
    def strategy(self, strategy: Strategy) -> None:
        if not isinstance(strategy, (Strategy, None)):
            raise TypeError("Invalid strategy object type")

        self.__strategy = strategy

    @stop_loss.setter
    def stop_loss(self, stop_loss: StopLossExit) -> None:
        if not isinstance(stop_loss, (StopLossExit, None)):
            raise TypeError("Invalid stop loss object type")

        self.__stop_loss = stop_loss

    @exit.setter
    def exit(self, exit: Exit) -> None:
        if not isinstance(exit, (Exit, None)):
            raise TypeError("Invalid stop loss object type")

        self.__exit = exit
    
    @account.setter
    def account(self, account: Account) -> None:
        if not isinstance(account, Account):
            raise TypeError("Invalid account type object")

        self.__account = account
            
    @shares.setter
    def shares(self, shares: int) -> None:
        if shares <= 0:
            raise ValueError("Shares cannot be equal or less than zero")

        self.__shares = shares

    def update_pnl(self, current_price: float):
        if self.position_type == "long":
            self.__pnl = (current_price - self.average_price) * self.shares
        else:
            self.__pnl = (self.average_price - current_price) * self.shares

    def increase_share(self, shares: int, price: float) -> None:
        if shares <= 0:
            raise ValueError("Shares cannot be equal or less than zero")
        self.__account.can_execute_trade()
        total_cost = self.__average_price * self.__shares + price * shares
        self.__shares += shares
        self.__average_price = total_cost / self.__shares
        self.__invested = self.__average_price * self.__shares