from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from utils import verify_password, DUMMY_HASH, hash_password
from db.session import get_session
from models.token_models import TokenBase, TokenData
from oauth2.oauth2 import create_access_token, verify_access_token
from dependancies.dependancies import get_current_user
from models.user_models import User, UserCreate, UserRead
from errors.errors_auth import InvalidCredentialsError, AuthenticationError

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
    session.commit()
    session.refresh(db_user)
    return db_user

@router.post("/login", response_model=TokenBase)
def login( userlogin : OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    """Login a user"""
    
    user = session.exec(select(User).where(User.email == userlogin.username)).first()
    if not user or not verify_password(userlogin.password, user.password):
        verify_password(userlogin.password, DUMMY_HASH)
        raise InvalidCredentialsError()
    
    access_token = create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}


