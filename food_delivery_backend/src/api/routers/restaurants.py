from fastapi import APIRouter, HTTPException, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.models import RestaurantCreate, Restaurant
from src.api.inmemory_db import restaurants, get_next_id

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", response_model=Restaurant, summary="Add new restaurant")
def create_restaurant(r: RestaurantCreate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    owner_id = int(Authorize.get_jwt_subject())
    rest_id = get_next_id("restaurant")
    restaurant = Restaurant(id=rest_id, owner_id=owner_id, **r.dict(), menus=[])
    restaurants[rest_id] = restaurant
    return restaurant

# PUBLIC_INTERFACE
@router.get("/", response_model=list[Restaurant], summary="List all restaurants")
def list_restaurants():
    return list(restaurants.values())

# PUBLIC_INTERFACE
@router.get("/{restaurant_id}", response_model=Restaurant, summary="Get restaurant details")
def get_restaurant(restaurant_id: int):
    if restaurant_id not in restaurants:
        raise HTTPException(status_code=404, detail="Restaurant not found")
    return restaurants[restaurant_id]
