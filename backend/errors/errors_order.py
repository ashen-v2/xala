from fastapi import HTTPException

class OrderNotFoundException(HTTPException):
    def __init__(self, detail: str = "Order not found"):
        super().__init__(status_code=404, detail=detail)