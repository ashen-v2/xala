from fastapi import APIRouter, Depends
from pydantic import EmailStr
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from utils import verify_password, DUMMY_HASH, hash_password
from db.session import get_session
from models.token_models import TokenBase, TokenData, passwordReset
from oauth2.oauth2 import create_access_token, create_password_reset_token, verify_password_reset_token
from dependancies.dependancies import get_current_user
from models.user_models import User, UserCreate, UserRead, UserUpdate
from errors.errors_auth import InvalidCredentialsError, UserNotFoundError, UserAlreadyExistsError
from errors.errors_db import DatabaseError


router : APIRouter = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserRead, status_code=201) 
async def create_user(user: UserCreate, session : Session =Depends(get_session)) -> UserRead:
    """Create a new user.
    Args:
        user (UserCreate): The user data to create.
        session (Session, optional): The database session. Defaults to Depends(get_session).
    Returns:
            UserRead: The created user.
     """
    db_user: User = User.model_validate(user)
    db_user.password = hash_password(user.password)
    session.add(db_user)
    try:
        session.commit()
    except IntegrityError:
        session.rollback()
        raise UserAlreadyExistsError()
    session.commit()

    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=TokenBase)
def login( userlogin : OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Login a user
    Args:
        userlogin (OAuth2PasswordRequestForm, optional): The login form data. Defaults to Depends().
        session (Session, optional): The database session. Defaults to Depends(get_session).
    Returns:
        TokenBase: The access token and token type."""
    
    user = session.exec(select(User).where(User.email == userlogin.username)).first()
    if not user or not verify_password(userlogin.password, user.password):
        verify_password(userlogin.password, DUMMY_HASH)
        raise InvalidCredentialsError()
    
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserRead, status_code=200)
def read_users_me(current_user: TokenData = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get the current logged in user.
    Args:
        current_user (TokenData, optional): The current user data from the token. Defaults to Depends(get_current_user).
        session (Session, optional): The database session. Defaults to Depends(get_session).
    Returns:
        UserRead: The current user data."""
    user = session.exec(select(User).where(User.id == current_user.user_id)).first()
    if not user:
        raise UserNotFoundError()
    return user

@router.patch("/me", response_model=UserRead, status_code=200)
def update_user_me(user_update: UserUpdate, current_user: TokenData = Depends(get_current_user), session: Session = Depends(get_session)):
    """Update the current logged in user.
    Args:
        user_update (UserCreate): The user data to update.
        current_user (TokenData, optional): The current user data from the token. Defaults to Depends(get_current_user).
        session (Session, optional): The database session. Defaults to Depends(get_session).
    Returns:
        UserRead: The updated user data."""
    user = session.exec(select(User).where(User.id == current_user.user_id)).first()
    if not user:
        raise UserNotFoundError()
    
    user_data = user_update.model_dump(exclude_unset=True)
    for key, value in user_data.items():
        setattr(user, key, value)

    session.add(user)
    try:
        session.commit()
    except Exception as e:
        session.rollback()
        raise DatabaseError("Failed to update user due to database error.")
    session.refresh(user)
    return user

@router.post("/forgot-password/{email}", status_code=200)
def forgot_password(email: EmailStr, session: Session = Depends(get_session)):
    """Initiate the password reset process for a user.
    Args:
        email (EmailStr): The email of the user who forgot their password.
        session (Session, optional): The database session. Defaults to Depends(get_session).
    Returns:
        passwordToken
    """
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise UserNotFoundError()
    
    reset_token = create_password_reset_token(data={"user_id": user.id})
    # Here you would typically send the reset token to the user's email address
    return {"password_token": reset_token}

@router.post("/reset-password", status_code=200)
def reset_password(password_reset: passwordReset, session: Session = Depends(get_session)):
    user_id = verify_password_reset_token(password_reset.password_token).user_id
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise UserNotFoundError()
    
    user.password = hash_password(password_reset.password)
    session.add(user)
    session.commit()
    return {"message": "Password reset successfully."}
