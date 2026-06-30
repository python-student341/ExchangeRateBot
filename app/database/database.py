from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
from fast_depends import Depends

from app.config import settings


engine = create_async_engine(settings.database, future=True, echo=False, poolclass=NullPool)

new_session = async_sessionmaker(autoflush=False, expire_on_commit=False, bind=engine)

async def get_session():
    async with new_session() as session:
        yield session

session_dep = Annotated[AsyncSession, Depends(get_session)]