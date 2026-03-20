from sqlmodel import SQLModel, Field
from datetime import datetime, timezone

class Cart(SQLModel, table=True):
    __tablename__ = "carts"
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(default=None, foreign_key="users.id")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class CartItem(SQLModel, table=True):
    __tablename__ = "cart_items"
    id: int = Field(default=None, primary_key=True)
    cart_id: int = Field(default=None, foreign_key="carts.id")
    product_id: int = Field(default=None, foreign_key="menu_items.id")
    quantity: int = Field(default=1)

class CartItemCreate(SQLModel):
    product_id: int
    quantity: int = 1

class CartItemRead(SQLModel):
    id: int
    cart_id: int
    product_id: int
    product_name: str
    quantity: int

class CartItemUpdate(SQLModel):
    quantity: int | None = None