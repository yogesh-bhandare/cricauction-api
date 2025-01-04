from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlayerRequest(BaseModel):
    first_name: str
    last_name: str
    img_url: str = None
    origin: str
    player_type: str
    points: int
    base_price: int
    is_sold: bool = False
    auction_id: int


class PlayerResponse(PlayerRequest):
    id: int
    sold_price: Optional[int] = None
    team_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)
