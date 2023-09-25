from sqlalchemy import Column, Integer, String, DateTime, JSON, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql import func


class Base(AsyncAttrs, DeclarativeBase):
    pass


class BinanceHistoryLastKeyRedis(Base):
    __tablename__ = "binance_history_last_key_redis"

    id = Column(Integer, primary_key=True)
    key = Column(String(255), nullable=False)
    time_created = Column(DateTime(timezone=True), server_default=func.now())


class Binance(Base):
    __tablename__ = "binance"

    id = Column(Integer, primary_key=True)
    e = Column(String(255), nullable=False)
    E = Column(BigInteger, nullable=False)
    s = Column(String(255), nullable=False)
    U = Column(BigInteger, nullable=False)
    u = Column(BigInteger, nullable=False)
    b = Column(JSON, nullable=True)
    a = Column(JSON, nullable=True)

    time_created = Column(DateTime(timezone=True), server_default=func.now())
