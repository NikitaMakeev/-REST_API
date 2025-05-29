import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))



import asyncio
from sqlalchemy import text
from config.database import async_engine, Base, async_session
from config.database import async_engine, Base, async_session
from models.user import User
from models.landmark import Landmark
from models.photo import Photo
from models.rating import Rating

async def init_db():
    try:
        print("🔄 Инициализация базы данных...")
        
        # Проверка соединения с БД
        async with async_engine.connect() as conn:
            await conn.execute(text("CREATE DATABASE IF NOT EXISTS wwlandmarks"))
            await conn.commit()
            print("✔ База данных доступна")

        # Создание таблиц
        async with async_engine.begin() as conn:
            print("🔨 Создание таблиц...")
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            print("✔ Таблицы созданы")

        # Добавление тестовых данных
        async with async_session() as session:
            async with session.begin():
                print("📝 Добавление тестовых данных...")
                
                # Пользователи
                user1 = User(
                    username='user1',
                    email='user1@example.com',
                    password=User.hash_password('user1_123')
                )
                user2 = User(
                    username='user2',
                    email='user2@example.com',
                    password=User.hash_password('user2_123')
                )
                session.add_all([user1, user2])
                await session.flush()

                # Достопримечательность
                landmark1 = Landmark(
                    name='Eiffel Tower',
                    description='The Eiffel Tower is a wrought-iron lattice tower in Paris, France.',
                    location='Paris',
                    country='France',
                    imageURL='https://example.com/eiffel.jpg',
                    user_id=user1.id
                )
                session.add(landmark1)
                await session.flush()

                # Фото
                photo1 = Photo(
                    url='https://example.com/eiffel_photo.jpg',
                    description='Beautiful view',
                    user_id=user1.id,
                    landmark_id=landmark1.id
                )
                session.add(photo1)

                # Рейтинг
                rating1 = Rating(
                    rating=5,
                    user_id=user1.id,
                    landmark_id=landmark1.id
                )
                session.add(rating1)

        print("✅ База данных успешно инициализирована!")
        
    except Exception as e:
        print(f"❌ Ошибка: {str(e)}")
        raise

if __name__ == '__main__':
    asyncio.run(init_db())