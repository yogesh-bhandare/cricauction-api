from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional

class PlayerType(str, Enum):
    USER = "user"
    TEAM = "team"
    ADMIN = "admin"

class UserRequest(BaseModel):
    username: EmailStr
    password: str
    role: PlayerType


class UserResponse(BaseModel):
    id: int
    username: str
    role: PlayerType
    model_config = ConfigDict(from_attributes=True)

