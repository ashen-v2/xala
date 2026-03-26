from fastapi import Depends, HTTPException
from models.token_models import TokenData
from oauth2.oauth2 import verify_access_token
from fastapi.security import OAuth2PasswordBearer
from errors.errors_token import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="v1/users/login")

def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    """Get the current user from the JWT access token.
    Args:
        token (str, optional): The JWT access token from the Authorization header. Defaults to Depends(oauth2_scheme).
        Returns:
        TokenData: The data extracted from the token, including user_id and expiration time."""
    try:
        payload = verify_access_token(token)
        user_id : int = payload.user_id
        if user_id is None:
            raise InvalidTokenError()
        return payload
    except Exception as e:
        raise InvalidTokenError()
    
