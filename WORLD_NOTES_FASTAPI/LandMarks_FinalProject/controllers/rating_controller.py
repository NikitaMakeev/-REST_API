from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, func
from fastapi import HTTPException
from models.rating import Rating
from models.landmark import Landmark
from schemas.rating_schema import RatingCreate, RatingUpdate
from models.user import User

async def add_rating(attraction_id: int, rating_data: RatingCreate, user: User, db: AsyncSession):
    # Проверяем, существует ли такая достопримечательность
    landmark = await db.get(Landmark, attraction_id)
    if not landmark:
        raise HTTPException(status_code=404, detail="Landmark not found")

    # Проверка на наличие оценки от этого пользователя
    result = await db.execute(
        select(Rating).where(Rating.user_id == user.id, Rating.landmark_id == attraction_id)
    )
    existing_rating = result.scalar_one_or_none()
    if existing_rating:
        raise HTTPException(status_code=400, detail="Rating already exists")

    new_rating = Rating(**rating_data.dict(), user_id=user.id, landmark_id=attraction_id)
    db.add(new_rating)
    await db.commit()
    await db.refresh(new_rating)
    return new_rating

# async def get_rating_by_id(rating_id: int, session: AsyncSession):
#     result = await session.execute(select(Rating).where(Rating.id == rating_id))
#     Rating = result.scalar_one_or_none()
#     if not Rating:
#         raise HTTPException(status_code=404, detail="Rating not found")
#     return Rating

async def get_average_rating(attraction_id: int, db: AsyncSession):
    result = await db.execute(
        select(func.avg(Rating.rating)).where(Rating.landmark_id == attraction_id)
    )
    avg_rating = result.scalar()
    return {"average_rating": round(avg_rating, 2) if avg_rating is not None else 0.0}

async def update_rating(attraction_id: int, rating_data: RatingUpdate, user: User, db: AsyncSession):
    result = await db.execute(
        select(Rating).where(Rating.user_id == user.id, Rating.landmark_id == attraction_id)
    )
    rating = result.scalar_one_or_none()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    rating.rating = rating_data.rating
    await db.commit()
    await db.refresh(rating)
    return rating

async def delete_rating(attraction_id: int, user: User, db: AsyncSession):
    result = await db.execute(
        select(Rating).where(Rating.user_id == user.id, Rating.landmark_id == attraction_id)
    )
    rating = result.scalar_one_or_none()
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")

    await db.delete(rating)
    await db.commit()
