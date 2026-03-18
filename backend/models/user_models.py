from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from datetime import datetime, timezone


class UserBase(SQLModel):
    name: str = Field(nullable=False)
    store_name: str = Field(nullable=False)
    email: EmailStr = Field(unique=True, nullable=False)
    password: str = Field(nullable=False)

class User(UserBase, table=True):
    __tablename__ = "users"
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
