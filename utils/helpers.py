from typing import Literal
from dataclasses import dataclass

@dataclass
class PositionSizingResult:
    rr: float 
    reward: float 
    risk: float
    position_size: int
    stop_loss: float
    exit: float
    
    def __str__(self) -> str:
        return f"RR : {self.rr}\nReward : {self.reward}\nRisk : {self.risk}\nPosition Size : {self.position_size}\nStop Loss : {self.stop_loss}\nExit : {self.exit}"

def position_sizing_calculator(stock_price:float, risk_percentage: float, tp: float, sl: float, value: float, position_type: Literal["long", "short"], average_price: float = None, total_shares: float = None) -> float:
    total = (average_price * total_shares) if average_price is not None else value
    total_risk = total * risk_percentage
    risk_per_share = stock_price * sl
    reward = stock_price * tp   
    risk = stock_price * sl

    return PositionSizingResult(reward=reward,
                                risk=risk,
                                rr=round((reward / risk), 2),
                                position_size=round(total_risk / risk_per_share),
                                stop_loss=(stock_price - risk if position_type == "long" else stock_price + risk),
                                exit=(stock_price + reward if position_type == "long" else stock_price - reward))

    