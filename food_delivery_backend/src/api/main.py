from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from fastapi.responses import JSONResponse
from src.api.routers import users, restaurants, menus, orders, payments, deliveries, reviews, notifications
from src.api.auth_config import Settings

# App-level OpenAPI metadata/tags for doc grouping
openapi_tags = [
    {"name": "Users", "description": "Operations for user registration, login, and profile management."},
    {"name": "Restaurants", "description": "Browse, search, and view restaurant details."},
    {"name": "Menus", "description": "View and query restaurant menu items."},
    {"name": "Orders", "description": "Place, check, and update orders."},
    {"name": "Payments", "description": "Payment workflows (mock/real)."},
    {"name": "Deliveries", "description": "Order delivery tracking endpoints."},
    {"name": "Reviews", "description": "Ratings and reviews endpoints."},
    {"name": "Notifications", "description": "Background notifications (order status, etc)."}
]

app = FastAPI(
    title="Food Delivery Backend API",
    description="Backend API for Food Delivery Platform. Provides authentication, orders, restaurants, menus, payments, deliveries, reviews.",
    version="1.0.0",
    openapi_tags=openapi_tags
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Auth config
@AuthJWT.load_config
def get_config():
    return Settings()


@app.exception_handler(AuthJWTException)
def auth_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.get("/", tags=["Health"])
def health_check():
    "API health check endpoint."
    return {"message": "Healthy"}

# --- Register Routers (API) ---
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(restaurants.router, prefix="/restaurants", tags=["Restaurants"])
app.include_router(menus.router, prefix="/menus", tags=["Menus"])
app.include_router(orders.router, prefix="/orders", tags=["Orders"])
app.include_router(payments.router, prefix="/payments", tags=["Payments"])
app.include_router(deliveries.router, prefix="/deliveries", tags=["Deliveries"])
app.include_router(reviews.router, prefix="/reviews", tags=["Reviews"])
app.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
