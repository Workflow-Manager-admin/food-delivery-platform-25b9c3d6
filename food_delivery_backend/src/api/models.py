from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

# PUBLIC_INTERFACE
class UserBase(BaseModel):
    """Base user model schema."""
    username: str = Field(..., description="Username")
    email: EmailStr = Field(..., description="Email address")
    full_name: Optional[str] = Field(None, description="Full name")
    is_active: bool = Field(default=True, description="Is the user active")
    is_restaurant: bool = Field(default=False, description="Is this user a restaurant owner?")

class UserCreate(UserBase):
    password: str = Field(..., description="Plain text password")

class UserLogin(BaseModel):
    username: str
    password: str

class UserInDB(UserBase):
    id: int
    password_hash: str

class UserProfile(UserBase):
    orders: Optional[list] = []

# --- Restaurant ---
class RestaurantBase(BaseModel):
    name: str
    description: Optional[str]
    address: str

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int
    owner_id: int
    menus: Optional[list] = []

# --- Menu & Items ---
class MenuBase(BaseModel):
    name: str
    restaurant_id: int

class Menu(MenuBase):
    id: int

class MenuItemBase(BaseModel):
    name: str
    description: Optional[str]
    price: float

class MenuItemCreate(MenuItemBase):
    menu_id: int

class MenuItem(MenuItemBase):
    id: int
    menu_id: int

# --- Orders ---
class OrderCreate(BaseModel):
    user_id: int
    restaurant_id: int
    items: List[int]  # MenuItem ids
    delivery_address: str

class Order(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    items: List[MenuItem]
    status: str
    total_price: float
    created_at: datetime
    updated_at: datetime
    delivery: Optional['Delivery'] = None

# --- Payment ---
class Payment(BaseModel):
    order_id: int
    amount: float
    status: str
    payment_method: str
    transaction_id: Optional[str]
    created_at: datetime

# --- Delivery ---
class Delivery(BaseModel):
    id: int
    order_id: int
    driver_id: Optional[int]
    status: str
    location: Optional[str]
    updated_at: datetime

# --- Reviews ---
class ReviewCreate(BaseModel):
    user_id: int
    restaurant_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str]

class Review(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime

# --- Notifications ---
class Notification(BaseModel):
    id: int
    user_id: int
    order_id: Optional[int]
    content: str
    read: bool
    created_at: datetime

Order.update_forward_refs()
