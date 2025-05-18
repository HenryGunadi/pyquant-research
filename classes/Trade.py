class Trade():
    def __init__(self, symbol: str):
        self.__symbol: str = symbol
        
        
    @property
    def symbol(self) -> str:
        return self.__symbol
    
    @symbol.setter
    def symbol(self, symbol: str) -> None:
        if not isinstance(symbol, str):
            raise TypeError("Symbol has to be a string.")

        self.__symbol = symbol
        
    
    
    