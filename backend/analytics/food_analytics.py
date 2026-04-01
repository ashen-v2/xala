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

    def get_weekly_sales(self, year: int = date.today().year, month: int = date.today().month):
        """Get weekly item sales for the current user within a month.
        args:
            year (int): The year for which to retrieve sales data.
            month (int): The month for which to retrieve sales data.
        returns:
            list of tuples containing week, item name, and total quantity sold."""
        week_label = func.date_trunc("week", Order.created_at).label("week")
        top_items = self.session.exec(
            select(week_label, MenuItem.name, func.sum(OrderItem.quantity).label("total_quantity"))
            .join(OrderItem, MenuItem.id == OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(Order.user_id == self.user_id)
            .where(extract("year", Order.created_at) == year)
            .where(extract("month", Order.created_at) == month)
            .group_by(MenuItem.name, week_label)
            .order_by(func.sum(OrderItem.quantity).desc())
        )
        return top_items

    def get_daily_sales(self, year: int = date.today().year, week: int = date.today().isocalendar()[1]):
        """Get daily item sales for the current user within an ISO week.
        args:
            year (int): The year for which to retrieve sales data.
            week (int): ISO week number.
        returns:
            list of tuples containing day, item name, and total quantity sold."""
        day_label = func.date_trunc("day", Order.created_at).label("day")
        top_items = self.session.exec(
            select(day_label, MenuItem.name, func.sum(OrderItem.quantity).label("total_quantity"))
            .join(OrderItem, MenuItem.id == OrderItem.product_id)
            .join(Order, Order.id == OrderItem.order_id)
            .where(Order.user_id == self.user_id)
            .where(extract("year", Order.created_at) == year)
            .where(extract("week", Order.created_at) == week)
            .group_by(MenuItem.name, day_label)
            .order_by(func.sum(OrderItem.quantity).desc())
        )
        return top_items
            