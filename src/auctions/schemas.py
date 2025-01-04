from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AuctionRequestSchema(BaseModel):
    name: str
    date: datetime 
    purse_amt: int
    min_bid: int
    bid_increase_by: int

class AuctionResponseSchema(AuctionRequestSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)