from datetime import datetime, date
from sqlmodel import Session
from sqlmodel import Session, select, func, extract
from models import Order
from errors.errors_date import DateError
from errors.errors_agent import InvalidInputError

class AiAnalytics:
    def __init__(self, session: Session, user_id: int):
        self.session = session
        self.user_id = user_id

    def get_sales_date_range(self, start_date: str, end_date: str, group_by: str = "month"):
        
        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError:
            raise DateError()

        match group_by:
            case "month":
                 date_label = func.date_trunc("month", Order.created_at).label("date")
            case "week":
                date_label = func.date_trunc("week", Order.created_at).label("date")
            case "day":
                date_label = func.date_trunc("day", Order.created_at).label("date")
            case _:
                raise InvalidInputError("Invalid group_by value. Expected 'month', 'week', or 'day'.")

        sales = self.session.exec(
            select( date_label, func.sum(Order.total_price).label("total_sales"))
            .where(Order.user_id == self.user_id)
            .where(Order.created_at >= start)
            .where(Order.created_at <= end)
            .group_by(date_label).order_by(date_label)
        ).all()
        return sales