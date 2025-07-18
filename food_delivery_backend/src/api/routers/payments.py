from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.models import Payment
from src.api.inmemory_db import payments, orders, get_next_id
from datetime import datetime

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", response_model=Payment, summary="Pay for an order (mock)")
def pay_for_order(order_id: int, payment_method: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    order = orders.get(order_id)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    if any(p.order_id == order_id for p in payments.values()):
        raise HTTPException(status_code=400, detail="Order already paid")
    pay_id = get_next_id("payment")
    now = datetime.utcnow()
    payment = Payment(
        order_id=order_id,
        amount=order.total_price,
        status="PAID",
        payment_method=payment_method,
        transaction_id=f"txn_{pay_id}",
        created_at=now
    )
    payments[pay_id] = payment
    # Mark order as 'Paid'
    order.status = "Paid"
    order.updated_at = now
    return payment
