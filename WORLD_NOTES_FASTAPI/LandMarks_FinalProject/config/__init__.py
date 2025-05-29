from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "mysql+asyncmy://root:@localhost:3306/wwlandmarks"

async_engine = create_async_engine(DATABASE_URL, echo=True)
Base = declarative_base()
async_session = sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession
)