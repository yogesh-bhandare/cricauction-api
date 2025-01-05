from pydantic import BaseModel, ConfigDict
from typing import Optional
from enum import Enum

class PlayerOrigin(str, Enum):
    OVERSEAS = "Overseas"
    NATIVE = "Native"

class PlayerType(str, Enum):
    BATSMAN = "Batsman"
    BOWLER = "Bowler"
    ALL_ROUNDER = "All Rounder"
    WICKET_KEEPER = "Wicket Keeper"

class PlayerRequest(BaseModel):
    first_name: str
    last_name: str
    img_url: str | None = None
    origin: PlayerOrigin = PlayerOrigin.NATIVE
    player_type: PlayerType
    points: int
    base_price: int
    is_sold: bool = False
    auction_id: int

class PlayerResponse(PlayerRequest):
    id: int
    sold_price: Optional[int] = None
    team_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)