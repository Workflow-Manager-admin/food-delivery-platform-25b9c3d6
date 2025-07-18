from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.models import UserCreate, UserLogin, UserProfile, UserInDB
from src.api.inmemory_db import users, get_next_id
from src.api.auth_config import hash_password, verify_password

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/register", response_model=UserProfile, summary="Register a new user")
def register_user(user: UserCreate):
    for u in users.values():
        if u.username == user.username or u.email == user.email:
            raise HTTPException(status_code=400, detail="Username/email already in use")
    user_id = get_next_id("user")
    user_obj = UserInDB(
        id=user_id,
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        is_active=True,
        is_restaurant=user.is_restaurant,
        password_hash=hash_password(user.password),
    )
    users[user_id] = user_obj
    return UserProfile(**user_obj.dict(exclude={"password_hash"}), orders=[])

# PUBLIC_INTERFACE
@router.post("/login", summary="Authenticate user and return JWT access token")
def login(user: UserLogin, Authorize: AuthJWT = Depends()):
    found_user = None
    for u in users.values():
        if u.username == user.username:
            found_user = u
            break
    if not found_user or not verify_password(user.password, found_user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    access_token = Authorize.create_access_token(subject=str(found_user.id))
    return {"access_token": access_token, "user_id": found_user.id}

# PUBLIC_INTERFACE
@router.get("/me", response_model=UserProfile, summary="Get the current user's profile")
def get_my_profile(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    if user_id not in users:
        raise HTTPException(status_code=404, detail="User not found")
    user = users[user_id]
    return UserProfile(**user.dict(exclude={"password_hash"}), orders=[])
