from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from models.token_models import TokenData
from db.session import get_session
from models.cart_models import Cart, CartItem, CartItemCreate, CartItemWithProduct, CartItemRead, CartItemUpdate
from models.menu_models import MenuItem
from dependancies.dependancies import get_current_user

router = APIRouter(prefix="/cart", tags=["cart"])


@router.post("/", status_code=201)
def add_to_cart(cartitem: CartItemCreate, session: Session = Depends(get_session), current_user : TokenData =Depends(get_current_user)):
    """Add an item to the cart."""
    # Check if the user already has a cart
    cart = session.exec(select(Cart).where(Cart.user_id == current_user.user_id)).first()
    if not cart:
        cart = Cart(user_id=current_user.user_id)
        session.add(cart)
        session.commit()
        session.refresh(cart)

    # Check if the item is already in the cart
    cart_item = session.exec(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == cartitem.product_id)).first()
    if cart_item:
        cart_item.quantity += cartitem.quantity
    else:
        cart_item = CartItem(cart_id=cart.id, product_id=cartitem.product_id, quantity=cartitem.quantity)
        session.add(cart_item)

    session.commit()
    return {"message": "Item added to cart"}

@router.get("/", response_model=list[CartItemRead], status_code=200)
def view_cart(session: Session = Depends(get_session), current_user : TokenData=Depends(get_current_user)):
    """View the contents of the cart."""
    cart = session.exec(select(Cart).where(Cart.user_id == current_user.user_id)).first()
    if not cart:
        return []
    cart_items = session.exec(select(CartItem, MenuItem).where(CartItem.cart_id == cart.id).join(MenuItem).where(CartItem.product_id == MenuItem.id)).all()
    return [{"id": c.id, "cart_id": c.cart_id, "product_id": c.product_id, "product_name": p.name, "quantity": c.quantity} for c, p in cart_items]

@router.delete("/{cart_item_id}", status_code=204)
def remove_from_cart(cart_item_id: int, session: Session = Depends(get_session), current_user : TokenData=Depends(get_current_user)):
    """Remove an item from the cart."""
    cart_item = session.exec(select(CartItem).where(CartItem.id == cart_item_id)).first()
    if not cart_item:
        return {"message": "Cart item not found"}
    cart = session.exec(select(Cart).where(Cart.id == cart_item.cart_id)).first()
    if cart.user_id != current_user.user_id:
        return {"message": "Not authorized to delete this item"}
    session.delete(cart_item)
    session.commit()
    return {"message": "Item removed from cart"}

@router.patch("/{cart_item_id}", status_code=200)
def update_cart_item(cart_item_id: int, cart_item_update: CartItemUpdate, session: Session = Depends(get_session), current_user : TokenData=Depends(get_current_user)):
    """Update the quantity of an item in the cart."""
    cart_item = session.exec(select(CartItem).where(CartItem.id == cart_item_id)).first()
    if not cart_item:
        return {"message": "Cart item not found"}
    cart = session.exec(select(Cart).where(Cart.id == cart_item.cart_id)).first()
    if cart.user_id != current_user.user_id:
        return {"message": "Not authorized to update this item"}
    if cart_item_update.quantity is not None:
        cart_item.quantity = cart_item_update.quantity
    session.commit()
    session.refresh(cart_item)
    return cart_item

