from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from ..players.schemas import PlayerResponseModel
from ..teams.schemas import TeamResponseSchema
from ..auctions.schemas import AuctionResponseSchema

class PlayerSoldRequest(BaseModel):
    sold_price: int
    auction_id: int
    player_id: int
    team_id: int


class TeamSummaryResponse(PlayerSoldRequest):
    id: int
    players: Optional[PlayerResponseModel] = None
    teams: Optional[TeamResponseSchema] = None
    auction: Optional[AuctionResponseSchema] = None

    model_config = ConfigDict(from_attributes=True)

class TeamPlayerSummary(BaseModel):
    team: TeamResponseSchema
    players: List[PlayerResponseModel]
    model_config = ConfigDict(from_attributes=True)
