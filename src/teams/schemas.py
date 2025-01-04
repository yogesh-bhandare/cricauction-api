from pydantic import BaseModel, ConfigDict
from typing import Optional

class TeamCreateRequest(BaseModel):
    name: str
    auction_id: int
    user_id: Optional[int] = None

class TeamUpdateRequest(TeamCreateRequest):
    remaining_purse: int = None


class TeamResponse(TeamCreateRequest):
    id: int
    remaining_purse: int
    model_config = ConfigDict(from_attributes=True)

class TeamRequest(BaseModel):
    username: str
    password: str
    role: str = "team"
