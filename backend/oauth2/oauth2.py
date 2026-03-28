from fastapi import HTTPException
import jwt
from config import settings
from models.token_models import TokenData
from datetime import datetime, timedelta, timezone

SECRET_KEY : str  = settings.secret_key
ALGORITHEM : str = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES : int = settings.access_token_expire_minutes


def create_access_token(data : dict):
    """Create a JWT access token."""
    to_encode : dict = data.copy()
    encoded_jwt : str = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHEM)
    return encoded_jwt

def verify_access_token(token: str) -> TokenData:
    """Verify the JWT access token and return the payload"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHEM])
        return TokenData(user_id=payload.get("user_id"), is_verified=payload.get("is_verified"))
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
def create_password_reset_token(data: dict):
    """Create a JWT token for password reset."""
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=10)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHEM)
    return encoded_jwt

def verify_password_reset_token(token: str) -> TokenData:
    """Verify the JWT password reset token and return the payload."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHEM])
        return TokenData(user_id=payload.get("user_id"))
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid or expired token") from e
    
def create_email_verification_token(data: dict):
    """Create a JWT token for email verification."""
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHEM)
    return encoded_jwt

def verify_email_verification_token(token: str) -> int:
    """Verify the JWT email verification token and return the user ID."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHEM])
        return payload.get("user_id")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e
    
    

