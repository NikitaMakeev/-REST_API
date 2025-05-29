from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from config.database import async_session
from middleware.auth import get_current_user
from models.user import User
from schemas.photo_schema import PhotoCreate, PhotoUpdate, PhotoResponse
import controllers.photo_controller as controller

router = APIRouter()

@router.get("/photos", response_model=list[PhotoResponse])
async def get_all():
    async with async_session() as session:
        return await controller.get_all_photos(session)

@router.get("/photos/{photo_id}", response_model=PhotoResponse)
async def get_one(photo_id: int):
    async with async_session() as session:
        return await controller.get_photo_by_id(photo_id, session)

@router.post("/photos", response_model=PhotoResponse, status_code=status.HTTP_201_CREATED)
async def create(data: PhotoCreate, user: User = Depends(get_current_user)):
    async with async_session() as session:
        return await controller.create_photo(data, user.id, session)

@router.put("/photos/{photo_id}", response_model=PhotoResponse)
async def update(photo_id: int, data: PhotoUpdate, user: User = Depends(get_current_user)):
    async with async_session() as session:
        return await controller.update_photo(photo_id, data, user.id, session)

@router.delete("/photos/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(photo_id: int, user: User = Depends(get_current_user)):
    async with async_session() as session:
        await controller.delete_photo(photo_id, user.id, session)
