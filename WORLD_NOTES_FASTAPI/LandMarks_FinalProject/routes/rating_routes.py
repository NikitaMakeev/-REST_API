from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import get_db
from schemas.rating_schema import RatingCreate, RatingUpdate, RatingResponse
from controllers import rating_controller
from middleware.auth import get_current_user
from models.user import User

router = APIRouter()

@router.post("/attractions/{attraction_id}/rating", response_model=RatingResponse, status_code=status.HTTP_201_CREATED)
async def create_rating(attraction_id: int, data: RatingCreate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await rating_controller.add_rating(attraction_id, data, user, db)

@router.get("/attractions/{attraction_id}/rating")
async def get_rating(attraction_id: int, db: AsyncSession = Depends(get_db)):
    return await rating_controller.get_average_rating(attraction_id, db)

# @router.get("/attractions/rating")
# async def get_rating_by_id (attraction_id: int, db: AsyncSession = Depends(get_db)):
#     return await rating_controller.get_average_rating(attraction_id, db)

@router.put("/attractions/{attraction_id}/rating", response_model=RatingResponse)
async def update_rating(attraction_id: int, data: RatingUpdate, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    return await rating_controller.update_rating(attraction_id, data, user, db)

@router.delete("/attractions/{attraction_id}/rating", status_code=status.HTTP_200_OK)
async def delete_rating(attraction_id: int, db: AsyncSession = Depends(get_db), user: User = Depends(get_current_user)):
    await rating_controller.delete_rating(attraction_id, user, db)
    return {"message": "Rating deleted"}
