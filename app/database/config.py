# from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+aiomysql://root:123456@192.168.50.199:3306/position"
engine = create_async_engine(DATABASE_URL, echo=True)
# 异步+同步
# SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, autoflush=False, autocommit=False)
# 异步
SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


async def get_db():
    async with SessionLocal() as db:
        yield db

async def close_all():
    await engine.dispose()
