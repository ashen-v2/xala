from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from db.session import get_session
from models.menu_models import MenuTable, MenuItem, MenuItemRead, MenuItemCreate
from dependancies.dependancies import get_current_user
from models.token_models import TokenData
from models.user_models import User
from errors.errors_auth import UserNotFoundError, AuthorizationError
from errors.errors_menu import MenuNotFoundError, ExceededMenuItemLimitError

router : APIRouter = APIRouter(prefix="/menu", tags=["menu"])

@router.get("/", response_model=list[MenuItemRead], status_code=200)
def read_menu_items(current_user: TokenData = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get all menu items of current user
    Args:
        current_user (TokenData, optional): The current user data from the token. Defaults to Depends(get_current_user).
        session (Session, optional): The database session. Defaults to Depends(get_session).
    Returns:
        list[MenuItemRead]: List of menu items for the current user."""
    user : User = session.get(User, current_user.user_id)
    if not user:
        raise UserNotFoundError()
    menu_id = session.exec(select(MenuTable.id).where(MenuTable.user_id == user.id)).first()
    if not menu_id:
        raise MenuNotFoundError()
    menu_items : list[MenuItem] = session.exec(select(MenuItem).where(MenuItem.menu_table_id == menu_id)).all()
    return menu_items

@router.get("/{item_id}", response_model=MenuItemRead, status_code=200)
def read_menu_item(item_id: int, current_user: TokenData = Depends(get_current_user), session: Session = Depends(get_session)):
    """Get a specific menu item by ID for the current user.
    Args:
        item_id (int): The ID of the menu item to retrieve.
    Returns:
        MenuItemRead: The requested menu item."""
    user : User = session.get(User, current_user.user_id)
    if not user:
        raise UserNotFoundError()
    menu_id = session.exec(select(MenuTable).where(MenuTable.user_id == user.id)).first()
    if not menu_id:
        raise MenuNotFoundError()
    menu_item : MenuItem = session.exec(select(MenuItem).where(MenuItem.id == item_id, MenuItem.menu_table_id == menu_id)).first()
    if not menu_item:
        raise MenuNotFoundError(detail="Menu item not found")
    if menu_item.menu_table_id != menu_id:
        raise AuthorizationError(detail="You are not authorized to access this menu item")
    return menu_item

@router.post("/", response_model=MenuItemRead, status_code=201)
def create_menu_item(menu_item: MenuItemCreate, current_user: TokenData = Depends(get_current_user), session: Session = Depends(get_session)):
    """Create a new menu item for the current user.
    Args:
        menu_item (MenuItemCreate): The menu item data to create.
    Returns:
        MenuItemRead: The created menu item."""
    user : User = session.get(User, current_user.user_id)
    if not user:
        raise UserNotFoundError()
    user_menu : MenuTable = session.exec(select(MenuTable).where(MenuTable.user_id == user.id)).first()
    if not user_menu:
        user_menu = MenuTable(user_id=user.id)
        session.add(user_menu)
        session.flush()
        session.refresh(user_menu)
        menu_id = user_menu.id
    else:
        menu_id = user_menu.id

    if user_menu.item_count >= 20:
        raise ExceededMenuItemLimitError()

    db_menu_item : MenuItemCreate = MenuItemCreate.model_validate(menu_item)
    menu_item : MenuItem = MenuItem(**db_menu_item.model_dump(), menu_table_id=menu_id)
    session.add(menu_item)
    user_menu.item_count += 1

    session.commit()
    session.refresh(menu_item)
    return menu_item