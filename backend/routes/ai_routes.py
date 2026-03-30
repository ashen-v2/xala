from fastapi import APIRouter, Depends, HTTPException
from typing import Any
from sqlmodel import Session
from models.token_models import TokenData
from models.user_models import User, UserAiRequests
from models.AiAgent_models import Prompt
from db.session import get_session
from dependancies.dependancies import get_current_user
from google import genai
from config import settings
from agent_tools.ai_analytics_tools import AiAnalytics
from agent_tools.ai_handler import get_sales_in_date_range
from datetime import datetime, timezone
from errors.errors_auth import UserNotVerifiedError, UserNotFoundError
from errors.errors_agent import AiRequestLimitExceededError


router = APIRouter(prefix="/ai", tags=["ai"])

@router.post("/analytics", status_code=200)
def ai_analytics(prompt: Prompt, session: Session = Depends(get_session), current_user: TokenData = Depends(get_current_user)):

    if not current_user.is_verified:
        raise UserNotVerifiedError()
    
    user : User = session.get(User, current_user.user_id)

    if not user:
        raise UserNotFoundError()
    
    if user.airequests and user.airequests.request_count >= 3:
        raise AiRequestLimitExceededError("You have exceeded the maximum number of AI requests. Please try again tommorrow.")

    #this is for adding time awarenes for llms, so that it can provide insights based on the current date and time.
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    day_name = datetime.now(timezone.utc).strftime("%A")

    prompt_text = prompt.data.strip()
    if not prompt_text:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty.")

    ai_analytics = AiAnalytics(session, current_user.user_id)
    def get_sales_data(start_date: str, end_date: str, group_by: str = "month") -> list[dict[str, object]]:
        """Get sales data for the current user within a date range.

        Args:
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.
            group_by: Grouping interval: day, week, or month.

        Returns:
            A list of grouped sales rows with date and total_sales.
        """
        return get_sales_in_date_range(ai_analytics, start_date, end_date, group_by)
    
    
    def get_top_items(start_date: str, end_date: str, group_by: str = "month") -> list[dict[str, Any]]:
        """Get top selling items for the current user within a date range.

        Args:
            start_date: Start date in YYYY-MM-DD format.
            end_date: End date in YYYY-MM-DD format.
            group_by: Grouping interval: day, week, or month.
        Returns:
            A list of grouped sales rows with date, item_name and total_quantity.
        """
        item_data = ai_analytics.get_item_sales_date_range(start_date, end_date, group_by)
        return [{"date": ms.date, "item_name": ms.name, "total_quantity": ms.total_quantity} for ms in item_data]

    client = genai.Client(api_key=settings.gemini_api_key)
    tools = [get_sales_data, get_top_items]
    config = genai.types.GenerateContentConfig(
        tools=tools,
        system_instruction=f"You are a helpful assistant that provides insights based on sales data." 
        f"Use the provided tools to fetch sales data and generate insights accordingly. Today is {day_name}, {today}."
        f"treat currency as LKR and provide insights in the context of a small street food business."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite-preview",
            contents=prompt_text,
            config=config,
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=502, detail="AI insights service is temporarily unavailable.")

    if not response.text:
        raise HTTPException(
            status_code=502,
            detail="Gemini returned a function call but no final insight text.",
        )
    
    user.airequests
    if not user.airequests:
        new_ai_requests = UserAiRequests(user_id=current_user.user_id, request_count=0)
        user.airequests = new_ai_requests
        session.add(user.airequests)
    if user.airequests.request_count >= 3:
        raise AiRequestLimitExceededError("You have exceeded the maximum number of AI requests. Please try again tommorrow.")
    user.airequests.request_count += 1
    user.airequests.last_request_time = datetime.now(timezone.utc)
    session.commit()
    return {"insights": response.text}
    




