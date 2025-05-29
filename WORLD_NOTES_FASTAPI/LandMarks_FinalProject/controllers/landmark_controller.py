# controllers/landmark_controller.py
from fastapi import HTTPException, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.landmark import Landmark
from models.rating import Rating
from schemas.landmark_schema import LandmarkCreate, LandmarkUpdate
from middleware.auth import get_current_user
from models.user import User
from config.database import async_session as async_session_maker
from sqlalchemy import func

async def get_all_landmarks_controller(country: str = None, sort: str = None):
    async with async_session_maker() as session:
        query = select(Landmark)

        if country:
            query = query.where(Landmark.country == country)

        landmarks = (await session.execute(query)).scalars().all()

        if sort == "rating":
            for landmark in landmarks:
                avg_rating_query = await session.execute(
                    select(func.avg(Rating.rating)).where(Rating.landmark_id == landmark.id)
                )
                landmark.avg_rating = avg_rating_query.scalar() or 0
            landmarks.sort(key=lambda x: x.avg_rating, reverse=True)

        return landmarks

async def get_landmark_controller(landmark_id: int):
    async with async_session_maker() as session:
        result = await session.execute(select(Landmark).where(Landmark.id == landmark_id))
        landmark = result.scalar_one_or_none()
        if not landmark:
            raise HTTPException(status_code=404, detail="Landmark not found")
        return landmark

async def create_landmark_controller(data: LandmarkCreate, user: User):
    async with async_session_maker() as session:
        new_landmark = Landmark(**data.dict(), user_id=user.id)
        session.add(new_landmark)
        await session.commit()
        await session.refresh(new_landmark)
        return new_landmark

async def update_landmark_controller(landmark_id: int, data: LandmarkUpdate, user: User):
    async with async_session_maker() as session:
        result = await session.execute(select(Landmark).where(Landmark.id == landmark_id))
        landmark = result.scalar_one_or_none()
        if not landmark:
            raise HTTPException(status_code=404, detail="Landmark not found")
        if landmark.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this landmark")

        for key, value in data.dict(exclude_unset=True).items():
            setattr(landmark, key, value)
        await session.commit()
        await session.refresh(landmark)
        return landmark

async def delete_landmark_controller(landmark_id: int, user: User):
    async with async_session_maker() as session:
        result = await session.execute(select(Landmark).where(Landmark.id == landmark_id))
        landmark = result.scalar_one_or_none()
        if not landmark:
            raise HTTPException(status_code=404, detail="Landmark not found")
        if landmark.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this landmark")
        await session.delete(landmark)
        await session.commit()
        return
