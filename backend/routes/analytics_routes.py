from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.session import get_session
from dependancies.dependancies import get_current_user
from models.token_models import TokenData
from analytics.sales_analytics import Analytics
from datetime import datetime
from models.analytics_models import MonthlySales, WeeklySales, DailySales
from analytics.food_analytics import FoodAnalytics

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/monthly-sales/{year}", status_code=200, response_model=list[MonthlySales])
def get_monthly_sales(year : int, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Get monthly sales data for the current user."""
    analytics = Analytics(session, current_user.user_id)
    monthly_sales = analytics.get_monthly_sales(year)
    monthly_sales : list[MonthlySales] = [MonthlySales(month=ms.month.strftime("%b"), total_sales=ms.total_sales) for ms in monthly_sales]
    return monthly_sales

@ router.get("/weekly-sales/{year}/{month}", status_code=200, response_model=list[WeeklySales])
def get_weekly_sales(year : int, month : int, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Get weekly sales data for the current user."""
    analytics = Analytics(session, current_user.user_id)
    weekly_sales = analytics.get_weekly_sales(year, month)
    weekly_sales : list[WeeklySales] = [WeeklySales(week=ws.week.strftime("%Y-%m-%d"), total_sales=ws.total_sales) for ws in weekly_sales]
    return weekly_sales

@ router.get("/daily-sales/{year}/{month}/{week}", status_code=200, response_model=list[DailySales])
def get_daily_sales(year : int, month : int, week : int, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Get daily sales data for the current user."""
    date_obj = datetime(year, month, week * 7)
    # Get the ISO week number
    week_number = date_obj.isocalendar()[1]
    analytics = Analytics(session, current_user.user_id)
    daily_sales = analytics.get_daily_sales(year,week_number)
    daily_sales : list[DailySales] = [DailySales(day=ds.day.strftime("%d-%a"), total_sales=ds.total_sales) for ds in daily_sales]
    return daily_sales

@router.get("/top-selling-items", status_code=200)
def get_top_selling_items(limit: int = 5, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Get the top selling items for the current user."""
    analytics = FoodAnalytics(session, current_user.user_id)
    top_items = analytics.get_top_selling_items(limit)
    return [{"item_name": item.name, "total_quantity": item.total_quantity} for item in top_items]

@router.get("/monthly-item-sales/{year}", status_code=200)
def get_monthly_item_sales(year: int, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Get monthly sales data for each item for the current user."""
    analytics = FoodAnalytics(session, current_user.user_id)
    monthly_item_sales = analytics.get_monthly_sales(year)
    return [{"month": mis.month.strftime("%b"), "item_name": mis.name, "total_quantity": mis.total_quantity} for mis in monthly_item_sales]