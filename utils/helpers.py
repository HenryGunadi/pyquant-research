from typing import Literal
from dataclasses import dataclass

@dataclass
class PositionSizingResult:
    rr: float 
    reward: float 
    risk: float
    position_size: int

def position_sizing_calculator(stock_price:float, average_price: float, total_shares: float, position_type: Literal["long", "short"], percentage: float, total_risk_percentage: float, sl: float) -> PositionSizingResult:
    total = average_price * total_shares
    total_risk = total * percentage
    risk_per_share = stock_price * sl

    if position_type.lower() == "long":
        position_size = round(total_risk / risk_per_share) # assuming its not a fractional shares


    