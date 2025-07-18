from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from src.api.models import ReviewCreate, Review
from src.api.inmemory_db import reviews, get_next_id
from datetime import datetime

router = APIRouter()

# PUBLIC_INTERFACE
@router.post("/", response_model=Review, summary="Submit a review for a restaurant")
def submit_review(review: ReviewCreate, Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    user_id = int(Authorize.get_jwt_subject())
    rev_id = get_next_id("review")
    now = datetime.utcnow()
    new_review = Review(
        id=rev_id,
        user_id=user_id,
        restaurant_id=review.restaurant_id,
        rating=review.rating,
        comment=review.comment,
        created_at=now
    )
    reviews[rev_id] = new_review
    return new_review

# PUBLIC_INTERFACE
@router.get("/restaurant/{restaurant_id}", response_model=list[Review], summary="List reviews for restaurant")
def list_reviews_for_restaurant(restaurant_id: int):
    return [r for r in reviews.values() if r.restaurant_id == restaurant_id]
