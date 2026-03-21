from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models.token_models import TokenData
from db.session import get_session
from dependancies.dependancies import get_current_user
from google import genai
from config import settings
from agent_tools.ai_analytics_tools import AiAnalytics
from agent_tools.ai_handler import get_sales_in_date_range
from agent_tools.gemini_tools import tools as genai_tools
from agent_tools.gemini_tools import get_sales_tool


router = APIRouter(prefix="/ai", tags=["ai"])

@router.get("/analytics", status_code=200)
def ai_analytics(session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):

    ai_analytics = AiAnalytics(session, current_user.user_id)
    def get_sales_data(start_date: str, end_date: str, group_by: str = "month"):
        return get_sales_in_date_range(ai_analytics, start_date, end_date, group_by)
    
    

    """Get AI-generated analytics insights based on the user's sales data."""
    client = genai.Client(api_key=settings.gemini_api_key)
    tools = genai.types.Tool(function_declarations=[get_sales_tool])
    prompt = "Generate a sales report for the current user based on their monthly sales data of year 2026."
    config = genai.types.GenerateContentConfig(tools=[tools],
        system_instruction="You are a helpful assistant that provides insights based on sales data. Use the provided tools to fetch sales data and generate insights accordingly."
    )

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=prompt,
        config=config
    )


    return {"insights": response}
    

