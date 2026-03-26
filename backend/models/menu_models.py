from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class MenuTable(SQLModel, table=True):
    __tablename__ = "user_menus"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(nullable=False, foreign_key="users.id")
    item_count: int = Field(default=0, nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class MenuItemBase(SQLModel):
    name: str = Field(nullable=False)
    description: str | None = None
    price: float = Field(nullable=False, ge=0.0)

class MenuItemCreate(MenuItemBase):
    pass

class MenuItemRead(MenuItemCreate):
    menu_table_id: int = Field(nullable=False, foreign_key="user_menus.id", ondelete="CASCADE")
    id: int = Field(default=None, primary_key=True)

class MenuItem(MenuItemRead, table=True):
    __tablename__ = "menu_items"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)

class MenuItemUpdate(SQLModel):
    name: str | None = None
    description: str | None = None
    price: float | None = None

    




