class Account():
    def __init__(self):
        self.__balance = 0
        self.__portfolio = None
        
    @property
    def balance(self) -> float:
        return self.__balance
    
    @balance.setter
    def balance(self, value: float) -> None:
        if value <= 0:
            raise ValueError("Value cannot be less or equal than zero")

        self.__balance += value