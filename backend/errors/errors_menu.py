from fastapi import HTTPException, status

class BaseMenuError(HTTPException):
    def __init__(self, detail: str = "Something went wrong with the Menu operation. Please try again later."):
        super().__init__(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=detail)

class MenuNotFoundError(HTTPException):
    def __init__(self, detail: str = "Menu not found"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)

class ExceededMenuItemLimitError(HTTPException):
    def __init__(self, detail: str = "You have reached the maximum number of menu items (20). Please delete some items before adding new ones."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
