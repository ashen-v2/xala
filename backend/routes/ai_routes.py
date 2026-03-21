from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from models.token_models import TokenData
from models.AiAgent_models import Prompt
from db.session import get_session
from dependancies.dependancies import get_current_user
from google import genai
from config import settings
from agent_tools.ai_analytics_tools import AiAnalytics
from agent_tools.ai_handler import get_sales_in_date_range


router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/analytics", status_code=200)
def ai_analytics(prompt : Prompt, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):

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
    
    
    def get_top_items(start_date: str, end_date: str, group_by: str = "month") -> list[dict[:str, str, int]]:
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
    prompt = prompt.data
    config = genai.types.GenerateContentConfig(
        tools=tools,
        system_instruction="You are a helpful assistant that provides insights based on sales data. Use the provided tools to fetch sales data and generate insights accordingly."
    )

    try:
        response = client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=prompt,
            config=config,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Gemini request failed: {exc}") from exc

    if not response.text:
        raise HTTPException(
            status_code=502,
            detail="Gemini returned a function call but no final insight text.",
        )

    return {"insights": response.text}



