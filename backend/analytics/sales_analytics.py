from sqlmodel import Session, select, func, extract
from models import Order
from datetime import date

class Analytics:
    def __init__(self, session: Session, user_id: int):
        self.session = session
        self.user_id = user_id

    def get_monthly_sales(self, year: int = date.today().year):
        month_label = func.date_trunc("month", Order.created_at).label("month")
        monthly_sales = self.session.exec(
            select( month_label, func.sum(Order.total_price).label("total_sales"))
            .where(Order.user_id == self.user_id)
            .where(extract("year", Order.created_at) == year)
            .group_by(month_label).order_by(month_label)
        )
        return monthly_sales
    
    def get_weekly_sales(self, year: int = date.today().year, month: int = date.today().month):
        week_label = func.date_trunc("week", Order.created_at).label("week")
        weekly_sales = self.session.exec(
            select(week_label, func.sum(Order.total_price).label("total_sales"))
            .where(Order.user_id == self.user_id)
            .where(extract("year", Order.created_at) == year)
            .where(extract("month", Order.created_at) == month)
            .group_by(week_label).order_by(week_label)
        )
        return weekly_sales
    
    def get_daily_sales(self, year: int = date.today().year, week: int = date.today().isocalendar()[1]):
        day_label = func.date_trunc("day", Order.created_at).label("day")
        daily_sales = self.session.exec(
            select(day_label, func.sum(Order.total_price).label("total_sales"))
            .where(Order.user_id == self.user_id)
            .where(extract("year", Order.created_at) == year)
            .where(extract("week", Order.created_at) == week)
            .group_by(day_label).order_by(day_label)
        )
        return daily_sales
