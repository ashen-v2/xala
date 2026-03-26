from fastapi import HTTPException, status

class CartItemNotFoundException(HTTPException):
    def __init__(self, detail: str = "Cart item not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)