from pydantic import BaseModel, ConfigDict
from typing import Optional

class TeamCreateRequestSchema(BaseModel):
    name: str
    auction_id: int


class TeamUpdateRequest(TeamCreateRequestSchema):
    remaining_purse: int


class TeamResponseSchema(TeamCreateRequestSchema):
    id: int
    remaining_purse: int
    model_config = ConfigDict(from_attributes=True)

