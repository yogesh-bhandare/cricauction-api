from pydantic import BaseModel, ConfigDict
from typing import Optional

class TeamCreateRequestSchema(BaseModel):
    name: str
    auction_id: int
    user_id: Optional[int] = None

class TeamUpdateRequest(TeamCreateRequestSchema):
    remaining_purse: int = None


class TeamResponseSchema(TeamCreateRequestSchema):
    id: int
    remaining_purse: int
    model_config = ConfigDict(from_attributes=True)

class TeamRequest(BaseModel):
    username: str
    password: str
    role: str = "team"
