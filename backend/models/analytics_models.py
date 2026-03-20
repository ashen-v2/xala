from sqlmodel import SQLModel, Field

class MonthlySales(SQLModel):
    month: str
    total_sales: float

class WeeklySales(SQLModel):
    week: str
    total_sales: float

class DailySales(SQLModel):
    day: str
    total_sales: float