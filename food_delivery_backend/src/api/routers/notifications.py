from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.models import Notification
from src.api.inmemory_db import notifications, get_next_id
from datetime import datetime

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", response_model=Notification, summary="Send a notification to a user (mock)")
def create_notification(
    user_id: int, content: str, order_id: int = None, Authorize: AuthJWT = Depends()
):
    Authorize.jwt_required()
    notif_id = get_next_id("notification")
    now = datetime.utcnow()
    notification = Notification(
        id=notif_id,
        user_id=user_id,
        order_id=order_id,
        content=content,
        read=False,
        created_at=now
    )
    notifications[notif_id] = notification
    return notification

# PUBLIC_INTERFACE
@router.get("/", response_model=list[Notification], summary="Get notifications for the current user")
def get_my_notifications(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    return [n for n in notifications.values() if n.user_id == user_id]
