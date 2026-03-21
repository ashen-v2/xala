from fastapi import HTTPException, status

class DateError(HTTPException):
    def __init__(self, detail: str = "Invalid date format. Expected format: YYYY-MM-DD."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)