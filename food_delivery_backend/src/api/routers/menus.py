from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.models import Menu, MenuItem, MenuItemCreate
from src.api.inmemory_db import menus, menu_items, restaurants, get_next_id

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", response_model=Menu, summary="Create a menu for a restaurant")
def create_menu(restaurant_id: int, name: str, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    menu_id = get_next_id("menu")
    menu = Menu(id=menu_id, name=name, restaurant_id=restaurant_id)
    menus[menu_id] = menu
    # Attach to restaurant's menus list
    rest = restaurants.get(restaurant_id)
    if rest:
        if not hasattr(rest, "menus") or rest.menus is None:
            rest.menus = []
        rest.menus.append(menu_id)
    return menu

# PUBLIC_INTERFACE
@router.post("/item", response_model=MenuItem, summary="Add menu item to a menu")
def add_menu_item(item: MenuItemCreate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    item_id = get_next_id("menu_item")
    menuitem = MenuItem(id=item_id, **item.dict())
    menu_items[item_id] = menuitem
    return menuitem

# PUBLIC_INTERFACE
@router.get("/", response_model=list[Menu], summary="List all menus")
def list_all_menus():
    return list(menus.values())

# PUBLIC_INTERFACE
@router.get("/restaurant/{restaurant_id}", response_model=list[MenuItem], summary="Get all menu items for a restaurant")
def get_menu_items_for_restaurant(restaurant_id: int):
    rest_menu_ids = [
        m.id for m in menus.values() if m.restaurant_id == restaurant_id
    ]
    items = [item for item in menu_items.values() if item.menu_id in rest_menu_ids]
    return items
