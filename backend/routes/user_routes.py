from fastapi import APIRouter, Depends
from sqlmodel import Session
from db.session import get_session
from models.user_models import User, UserCreate, UserRead

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
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

