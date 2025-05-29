from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.photo import Photo
from schemas.photo_schema import PhotoCreate, PhotoUpdate

async def get_all_photos(session: AsyncSession):
    result = await session.execute(select(Photo))
    return result.scalars().all()

async def get_photo_by_id(photo_id: int, session: AsyncSession):
    result = await session.execute(select(Photo).where(Photo.id == photo_id))
    photo = result.scalar_one_or_none()
    if not photo:
        raise HTTPException(status_code=404, detail="Photo not found")
    return photo

async def create_photo(data: PhotoCreate, user_id: int, session: AsyncSession):
    new_photo = Photo(**data.dict(), user_id=user_id)
    session.add(new_photo)
    await session.commit()
    await session.refresh(new_photo)
    return new_photo

async def update_photo(photo_id: int, data: PhotoUpdate, user_id: int, session: AsyncSession):
    photo = await get_photo_by_id(photo_id, session)
    if photo.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this photo")

    for key, value in data.dict(exclude_unset=True).items():
        setattr(photo, key, value)

    await session.commit()
    await session.refresh(photo)
    return photo

async def delete_photo(photo_id: int, user_id: int, session: AsyncSession):
    photo = await get_photo_by_id(photo_id, session)
    if photo.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this photo")
    await session.delete(photo)
    await session.commit()
