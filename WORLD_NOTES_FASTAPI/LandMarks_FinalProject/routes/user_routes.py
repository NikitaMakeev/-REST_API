from fastapi import APIRouter, Depends, HTTPException
from config.database import get_db
from sqlalchemy.orm import Session
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from controllers.user_controller import create_user, authenticate_user, get_user, get_users, delete_user, update_user , get_current_user
from models.user import User
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter()

# Регистрация пользователя
@router.post("/users/auth/register")
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return await create_user(user, db)

# Вход пользователя
@router.post("/users/auth/login")
async def login(user: UserCreate, db: Session = Depends(get_db)):
    return await authenticate_user(user, db)

# Получение всех пользователей
@router.get("/users", response_model=List[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    return await get_users(db)

# Получение одного пользователя
@router.get("/users/{user_id}", response_model=UserResponse)
async def get_single_user(user_id: int, db: Session = Depends(get_db)):
    return await get_user(user_id, db)

# Удаление пользователя
@router.delete("/users/{user_id}", response_model=UserResponse)
async def remove_user(user_id: int, db: Session = Depends(get_db)):
    return await delete_user(user_id, db)


@router.put("/users/{user_id}")
async def update_user_data(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)  # Получаем текущего пользователя
):
    return await update_user(user_id, user_update, db, current_user)