from fastapi import HTTPException, status

class InvalidInputError(HTTPException):
    def __init__(self, detail: str = "Invalid input provided. Please check your data and try again."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)

class AiRequestLimitExceededError(HTTPException):
    def __init__(self, detail: str = "AI request limit exceeded. Please wait before making more requests."):
        super().__init__(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=detail)