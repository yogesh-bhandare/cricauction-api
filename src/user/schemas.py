from pydantic import BaseModel, EmailStr, ConfigDict

class UserRequest(BaseModel):
    username: EmailStr
    password: str
    role: str

class UserResponse(BaseModel):
    id: int
    username: EmailStr
    role: str
    model_config = ConfigDict(from_attributes=True)