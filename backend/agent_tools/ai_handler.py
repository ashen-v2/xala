from fastapi import APIRouter, Depends
from sqlmodel import Session
from agent_tools.ai_analytics_tools import AiAnalytics
from db.session import get_session
from dependancies.dependancies import get_current_user
from models.token_models import TokenData
from agent_tools.ai_analytics_tools import AiAnalytics


def get_sales_in_date_range( ai_analytics: AiAnalytics, start_date: str, end_date: str, group_by: str = "month"):
    """
Get sales data for a specific date range, grouped by month, week, or day.

Args:
    start_date: The start date in 'YYYY-MM-DD' format.
    end_date: The end date in 'YYYY-MM-DD' format.
    group_by: The interval to group by ('month', 'week', or 'day').
    
Returns:
    A list of dictionaries. Each dictionary contains:
    - "date": The start date of the period (string).
    - "total_sales": The sum of sales for that period (float).
"""
    sales_data = ai_analytics.get_sales_date_range(start_date, end_date, group_by)
    return [{"date": ms[0], "total_sales": ms[1]} for ms in sales_data]
