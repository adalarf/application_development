from pydantic import BaseModel, ConfigDict
from uuid import UUID
from app.db import User


class UserCreate(BaseModel):
    username: str
    email: str
    description: str | None = None


class UserUpdate(BaseModel):
    username: str | None = None
    email: str | None = None
    description: str | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    username: str
    email: str
    description: str | None = None


class UserListResponse(BaseModel):
    users: list[UserResponse]
    users_count: int
