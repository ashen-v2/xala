
get_sales_tool = {
    "name": "get_sales_data",
    "description": "Get sales data between two dates grouped by day, week, or month.",
    "parameters": {
        "type": "object",
        "properties": {
            "start_date": {"type": "string"},
            "end_date": {"type": "string"},
            "group_by": {
                "type": "string",
                "enum": ["day", "week", "month"]
            }
        },
        "required": ["start_date", "end_date"]
    }
}

tools = [{
    "function_declarations": [get_sales_tool]
}]