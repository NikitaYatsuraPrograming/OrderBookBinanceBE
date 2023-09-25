
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from settings.db_setting import SQLALCHEMY_URL, SQLALCHEMY_URL_ALEMBIC

engine = create_async_engine(SQLALCHEMY_URL,
                             future=True,
                             echo=True)

sync_engine = create_engine(SQLALCHEMY_URL_ALEMBIC)


# expire_on_commit=False will prevent attributes from being expired
# after commit.
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Dependency
async def get_db() -> AsyncSession:
    async with async_session() as session:
        # logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session
