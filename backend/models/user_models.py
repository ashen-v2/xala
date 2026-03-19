from sqlmodel import SQLModel, Field
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
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class UserRead(UserBase):
    id: int

class UserUpdate(SQLModel):
    name: str | None = None
    store_name: str | None = None



