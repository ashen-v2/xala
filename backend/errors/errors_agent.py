from fastapi import HTTPException, status

class InvalidInputError(HTTPException):
    def __init__(self, detail: str = "Invalid input provided. Please check your data and try again."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)