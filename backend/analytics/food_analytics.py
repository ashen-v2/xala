from sqlmodel import Session, select, func, extract
from models import OrderItem, MenuItem, Order
from datetime import date

class FoodAnalytics:
    def __init__(self, session: Session, user_id: int):
        self.session = session
        self.user_id = user_id

    def get_top_selling_items(self, limit: int = 5):
        """Get the top selling items for the current user.
        args:
            limit (int): The maximum number of top items to return. Defaults to 5.
        returns:
            list of tuples containing item name and total quantity sold."""
        top_items = self.session.exec(
            select(MenuItem.name, func.sum(OrderItem.quantity).label("total_quantity"))
            .join(OrderItem, MenuItem.id == OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(Order.user_id == self.user_id)
            .group_by(MenuItem.name)
            .order_by(func.sum(OrderItem.quantity).desc())
            .limit(limit)
        ).all()
        return top_items
    
    def get_monthly_sales(self, year: int = date.today().year):
        """Get monthly sales data for the current user.
        args:
            year (int): The year for which to retrieve sales data. Defaults to the current year
        returns:
            list of tuples containing month, item name, and total quantity sold."""
        month_label = func.date_trunc("month", Order.created_at).label("month")
        top_items = self.session.exec(
        select(month_label,MenuItem.name, func.sum(OrderItem.quantity).label("total_quantity"))
        .join(OrderItem, MenuItem.id == OrderItem.product_id)
        .join(Order, Order.id == OrderItem.order_id)
        .where(Order.user_id == self.user_id)
        .where(extract("year", Order.created_at) == year)
        .group_by(MenuItem.name, month_label)
        .order_by(func.sum(OrderItem.quantity).desc()))
        return top_items
            