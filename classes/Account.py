from .Portfolio import Portfolio

class Account():
    def __init__(self, balance: float):
        self.balance = balance
        self.__portfolio: Portfolio = Portfolio()
        
    @property
    def balance(self) -> float:
        return self.__balance
    
    @property
    def portfolio(self) -> Portfolio:
        return self.__portfolio
    
    @balance.setter
    def balance(self, value: float = 0) -> None:
        if value < 0:
            raise ValueError("Value cannot be less or equal than zero")

        self.__balance = value

    def edit_balance(self, add: bool, value: float) -> None:
        if add:
            self.__balance += value
        elif not add:
            if self.__balance < value:
                raise ValueError("Balance is not enough")
            
            self.__balance -= value