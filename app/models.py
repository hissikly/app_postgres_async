from sqlalchemy import  Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
import datetime
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker


Base = declarative_base()


class Seller(Base):
    __tablename__ = "sellers"

    id = Column(Integer, primary_key=True)
    sellername = Column(String, index=True, unique=True)


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, nullable=False)
    desc = Column(String)
    price = Column(Integer, index=True, nullable=False)
    date = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    is_actual = Column(Boolean, default=True)

    seller_id = Column(Integer, ForeignKey("sellers.id"))


DATABASE_URL = "postgresql+asyncpg://postgres:example@db:5432/Store"

engine = create_async_engine(DATABASE_URL, echo=True)
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

async def get_session():
    async with async_session() as session:
        yield session
