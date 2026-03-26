from sqlmodel import SQLModel, Field
from datetime import datetime, timezone


class OrderBase(SQLModel):
    user_id: int = Field(default=None, foreign_key="users.id", ondelete="CASCADE")
    total_price: float = Field(default=0.0, ge=0.0)

class OrderCreate(OrderBase):
    pass

class OrderRead(OrderBase):
    id: int = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Order(OrderRead, table=True):
    __tablename__ = "orders"

class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"
    id: int = Field(default=None, primary_key=True)
    order_id: int = Field(default=None, foreign_key="orders.id", ondelete="CASCADE")
    product_id: int = Field(default=None, foreign_key="menu_items.id", ondelete="CASCADE")
    quantity: int = Field(default=1, ge=1)
    price: float = Field(default=0.0, ge=0.0)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class OrderItemRead(SQLModel):
    id: int
    order_id: int
    product_id: int
    product_name: str
    quantity: int
    price: float
    created_at: datetime
