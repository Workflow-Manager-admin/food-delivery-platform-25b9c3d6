from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.models import Delivery
from src.api.inmemory_db import deliveries, orders, get_next_id
from datetime import datetime

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", response_model=Delivery, summary="Create delivery for an order")
def create_delivery(order_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if any(delivery_.order_id == order_id for delivery_ in deliveries.values()):
        raise HTTPException(status_code=400, detail="Delivery already exists for this order")
    del_id = get_next_id("delivery")
    now = datetime.utcnow()
    delivery = Delivery(
        id=del_id,
        order_id=order_id,
        driver_id=None,
        status="En Route",
        location="Restaurant",
        updated_at=now
    )
    deliveries[del_id] = delivery
    order.delivery = delivery
    return delivery

# PUBLIC_INTERFACE
@router.get("/order/{order_id}", response_model=Delivery, summary="Get delivery details for order")
def get_delivery_for_order(order_id: int, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    for d in deliveries.values():
        if d.order_id == order_id:
            return d
    raise HTTPException(status_code=404, detail="Delivery not found for this order")
