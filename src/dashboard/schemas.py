from pydantic import BaseModel
from ..auctions.schemas import AuctionResponseSchema
from ..teams.schemas import TeamResponseSchema
from ..players.schemas import PlayerResponseModel

class DashboardResponse(BaseModel):
    auction: AuctionResponseSchema
    teams: TeamResponseSchema
    players: PlayerResponseModel