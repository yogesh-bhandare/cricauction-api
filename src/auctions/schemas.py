from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AuctionRequest(BaseModel):
    name: str
    date: datetime 
    purse_amt: int
    min_bid: int
    bid_increase_by: int

class AuctionResponse(AuctionRequest):
    id: int
    model_config = ConfigDict(from_attributes=True)
