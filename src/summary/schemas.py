from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from ..players.schemas import PlayerResponse
from ..teams.schemas import TeamResponse
from ..auctions.schemas import AuctionResponse

class PlayerSoldRequest(BaseModel):
    sold_price: int
    auction_id: int
    player_id: int
    team_id: int


class TeamSummaryResponse(PlayerSoldRequest):
    id: int
    players: Optional[PlayerResponse] = None
    teams: Optional[TeamResponse] = None
    auction: Optional[AuctionResponse] = None

    model_config = ConfigDict(from_attributes=True)

class TeamPlayerSummary(BaseModel):
    team: TeamResponse
    players: List[PlayerResponse]
    model_config = ConfigDict(from_attributes=True)
