from pydantic import BaseModel, ConfigDict
from typing import Optional

class PlayerSoldRequest(BaseModel):
    sold_price: int
    auction_id: int
    player_id: int
    team_id: int


class TeamSummaryResponse(PlayerSoldRequest):
    id: int
    model_config = ConfigDict(from_attributes=True)

