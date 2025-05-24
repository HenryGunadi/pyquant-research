from typing import List
from Trade import Trade

class Portfolio():
    def __init__(self):
        self.__holdings: List[Trade] = []
        
    @property
    def holdings(self) -> List[Trade]:
        return self.__holdings
    
    @holdings.setter
    def holdings(self, trade: Trade) -> None:
        if not isinstance(trade, Trade):
            raise TypeError("Invalid trade object")
        
        self.__holdings.append(trade)
        
    def remove_trade(self, id: str):
        for trade in self.__holdings:
            if trade.id == id:
                self.__holdings.remove(trade)