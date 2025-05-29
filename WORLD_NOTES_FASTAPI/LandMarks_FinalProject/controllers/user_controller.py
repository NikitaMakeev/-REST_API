from sqlalchemy.future import select
from fastapi import HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends
from models import User
from schemas.user_schema import UserCreate, UserUpdate, UserResponse
from middleware.auth import get_current_user
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import jwt
from decouple import config

SECRET_KEY = config("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Создание нового пользователя
async def create_user(user: UserCreate, db: AsyncSession):
    # Проверка на существующий email
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()
    
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Создание нового пользователя с хешированным паролем
    new_user = User(
        username=user.username,
        email=user.email,
        password=bcrypt.hash(user.password)  # Хешируем пароль
    )
    
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    
    return UserResponse(id=new_user.id, username=new_user.username, email=new_user.email)

# Аутентификация пользователя
async def authenticate_user(user: UserCreate, db: AsyncSession):
    result = await db.execute(select(User).filter(User.email == user.email))
    existing_user = result.scalars().first()

    if not existing_user or not bcrypt.verify(user.password, existing_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token({"sub": str(existing_user.id)}) 
    return {
    "access_token": access_token,
    "token_type": ""
}

# Создание JWT токена
def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Получить одного пользователя
async def get_user(user_id: int, db: Session):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Получить всех пользователей
async def get_users(db: Session):
    result = await db.execute(select(User))
    return result.scalars().all()

# Удалить пользователя
async def delete_user(user_id: int, db: AsyncSession):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()

    return user  # показываем кого удалили

# Обновить данные пользователя
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession,
    current_user: User
):
    # Проверка, что текущий пользователь обновляет только свои данные
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    # Получаем пользователя из базы данных
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Обновляем данные пользователя
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    await db.commit()
    await db.refresh(user)
    
    return user

