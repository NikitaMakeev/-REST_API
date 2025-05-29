from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# Используем asyncmy драйвер для асинхронного MySQL
DATABASE_URL = "mysql+asyncmy://root:@localhost:3306/wwlandmarks"

# Создаем асинхронный движок с явным указанием пула соединений
async_engine = create_async_engine(
    DATABASE_URL,
    echo=True,  # Логируем SQL-запросы
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True  # Проверяем соединения перед использованием
)

# Настройка сессии
async_session = sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False
)

# Базовый класс для моделей
Base = declarative_base()

# Асинхронная функция для получения сессии
async def get_db():
    async with async_session() as session:
        yield session
