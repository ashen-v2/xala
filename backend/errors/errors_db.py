from fastapi import HTTPException, status

class DatabaseError(HTTPException):
    def __init__(self, detail: str = "An error occurred while accessing the database"):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)