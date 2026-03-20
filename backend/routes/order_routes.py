from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from errors.errors_auth import AuthorizationError
from errors.errors_order import OrderNotFoundException
from db.session import get_session
from models.order_models import Order, OrderItem, OrderCreate, OrderRead, OrderItemRead
from models.cart_models import Cart, CartItem
from models.menu_models import MenuItem
from models.token_models import TokenData
from dependancies.dependancies import get_current_user

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderRead, status_code=201)
def create_order(session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Create a new order from the user's cart."""
    # Get the user's cart
    cart = session.exec(select(Cart).where(Cart.user_id == current_user.user_id)).first()
    if not cart:
        return {"message": "Cart is empty"}

    # Create the order
    order = Order(user_id=current_user.user_id, total_price=0.0)
    session.add(order)
    session.flush()
    session.refresh(order)

    # Add items to the order and calculate total price
    total_price = 0.0
    cart_items = session.exec(select(CartItem,MenuItem).where(CartItem.cart_id == cart.id).join(MenuItem).where(MenuItem.id == CartItem.product_id)).all()
    for cart_item, menu_item in cart_items:
        if menu_item:
            item_total = menu_item.price * cart_item.quantity
            total_price += item_total
            order_item = OrderItem(order_id=order.id, product_id=cart_item.product_id, quantity=cart_item.quantity, price=item_total)
            session.add(order_item)

    # Update the order's total price
    order.total_price = total_price


    # Clear the user's cart
    for cart_item, menu_item in cart_items:
        session.delete(cart_item)
    session.commit()
    session.refresh(order)

    return order

@router.get("/", response_model=list[OrderRead], status_code=200)
def get_orders(session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user), limit: int = 50, skip: int = 0):
    """Get a list of the user's orders."""
    orders = session.exec(select(Order).where(Order.user_id == current_user.user_id).offset(skip).limit(limit)).all()
    if orders and current_user.user_id != orders[0].user_id:
        return AuthorizationError(detail="Not authorized to view this orders")
    return orders

@router.get("/{order_id}", response_model=OrderRead, status_code=200)
def get_order(order_id: int, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Get details of a specific order."""
    order = session.exec(select(Order).where(Order.id == order_id, Order.user_id == current_user.user_id)).first()
    if not order:
        raise OrderNotFoundException()
    if current_user.user_id != order.user_id:
        return AuthorizationError(detail="Not authorized to view this order")
    return order

@router.get("/{order_id}/items", response_model=list[OrderItemRead], status_code=200)
def get_order_items(order_id: int, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Get the items in a specific order."""
    order = session.exec(select(Order).where(Order.id == order_id, Order.user_id == current_user.user_id)).first()
    if not order:
        raise OrderNotFoundException()
    if current_user.user_id != order.user_id:
        return AuthorizationError(detail="Not authorized to view this order")
    order_items = session.exec(select(OrderItem, MenuItem).where(OrderItem.order_id == order.id).join(MenuItem).where(MenuItem.id == OrderItem.product_id)).all()
    order_items_read : list[OrderItemRead] = []
    for oi, mi in order_items:
        order_items_read.append(OrderItemRead(
            id=oi.id,
            order_id=oi.order_id,
            product_id=oi.product_id,
            product_name=mi.name,
            quantity=oi.quantity,
            price=oi.price,
            created_at=oi.created_at
        ))
    return order_items_read

@router.delete("/{order_id}", status_code=204)
def delete_order(order_id: int, session: Session = Depends(get_session), current_user : TokenData = Depends(get_current_user)):
    """Delete a specific order."""
    order = session.exec(select(Order).where(Order.id == order_id, Order.user_id == current_user.user_id)).first()
    if not order:
        raise OrderNotFoundException()
    if current_user.user_id != order.user_id:
        raise AuthorizationError(detail="Not authorized to delete this order")
    session.delete(order)
    session.commit()
    return

