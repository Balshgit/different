from asyncio import current_task
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_scoped_session,
    create_async_engine,
)
from sqlalchemy.orm import Session, sessionmaker

from settings import settings

async_engine: AsyncEngine = create_async_engine(str(settings.async_db_url), echo=settings.DB_ECHO)
async_session_factory = async_scoped_session(
    sessionmaker(  # type: ignore
        autocommit=False,
        autoflush=False,
        class_=AsyncSession,
        expire_on_commit=False,
        bind=async_engine,
    ),
    scopefunc=current_task,
)


sync_engine = create_engine(settings.sync_db_url, echo=settings.DB_ECHO)
sync_session_factory = sessionmaker(sync_engine)


def get_sync_db_session() -> Session:
    session: Session = sync_session_factory()
    try:
        return session
    except Exception:
        session.rollback()
        raise
    finally:
        session.commit()
        session.close()


@asynccontextmanager
async def get_async_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Create and get database session.

    :param request: current request.
    :yield: database session.
    """
    session = async_session_factory()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.commit()
        await session.close()
        await async_session_factory.remove()
