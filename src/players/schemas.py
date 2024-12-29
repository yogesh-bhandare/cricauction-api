from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlayerRequestModel(BaseModel):
    first_name: str
    last_name: str
    origin: str
    player_type: str
    points: int
    base_price: int
    is_sold: bool = False
    auction_id: int


class PlayerResponseModel(PlayerRequestModel):
    sold_price: Optional[int] = None
    id: int
    team_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)