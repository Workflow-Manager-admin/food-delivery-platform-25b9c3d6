from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi_jwt_auth import AuthJWT
from src.api.models import OrderCreate, Order
from src.api.inmemory_db import orders, get_next_id, menu_items
from datetime import datetime

router = APIRouter()

def calculate_total_price(item_ids):
    return sum(menu_items[i].price for i in item_ids if i in menu_items)

def fake_background_order_processing(order_id: int):
    """Pretend to process an order asynchronously (update status, etc)."""
    import time
    import random
    # simulate status updates
    statuses = ["Processing", "Cooking", "Ready", "Picked Up", "Delivered"]
    for status in statuses[1:]:
        time.sleep(random.uniform(0.2, 0.5))
        order = orders.get(order_id)
        if order:
            order.status = status
            order.updated_at = datetime.utcnow()

# PUBLIC_INTERFACE
@router.post("/", response_model=Order, summary="Place a new order (with background task)")
def place_order(
    o: OrderCreate,
    BackgroundTasks: BackgroundTasks,
    Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    order_id = get_next_id("order")
    items = [menu_items[item_id] for item_id in o.items if item_id in menu_items]
    total = calculate_total_price(o.items)
    now = datetime.utcnow()
    order = Order(
        id=order_id,
        user_id=user_id,
        restaurant_id=o.restaurant_id,
        items=items,
        status="Placed",
        total_price=total,
        created_at=now,
        updated_at=now,
        delivery=None,
    )
    orders[order_id] = order
    BackgroundTasks.add_task(fake_background_order_processing, order_id)
    return order

# PUBLIC_INTERFACE
@router.get("/", response_model=list[Order], summary="Get my orders")
def get_my_orders(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    out = [o for o in orders.values() if o.user_id == user_id]
    return out

# PUBLIC_INTERFACE
@router.get("/{order_id}", response_model=Order, summary="Get order by ID")
def get_order(order_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
