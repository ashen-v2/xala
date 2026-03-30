from sqlmodel import Relationship, SQLModel, Field
from pydantic import EmailStr
from datetime import datetime, timezone


class UserBase(SQLModel):
    name: str = Field(nullable=False)
    store_name: str = Field(nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)

class UserCreate(UserBase):
    password: str = Field(nullable=False)

class User(UserCreate, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    verified: bool = Field(default=False, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    airequests : "UserAiRequests" = Relationship(back_populates="user")

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: str | None = None
    store_name: str | None = None

class UserAiRequests(SQLModel, table=True):
    __tablename__ = "user_ai_request_counts"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    request_count: int = Field(default=0, nullable=False, lt=6)
    last_request_time: datetime | None = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    user: User = Relationship(back_populates="airequests")



