"""
Database Connection and Session Management
Production-ready async PostgreSQL setup with SQLAlchemy 2.0.
"""

import logging
from typing import AsyncGenerator, Optional

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)

from app.config.settings import get_settings

logger = logging.getLogger(__name__)

_engine: Optional[AsyncEngine] = None
_session_factory: Optional[async_sessionmaker] = None


async def init_db() -> None:
    """
    Initialize database engine and session factory.
    Must be called at application startup.
    """
    global _engine, _session_factory

    settings = get_settings()

    logger.info(
        f"Initializing database connection to "
        f"{settings.database_url.split('@')[1] if '@' in settings.database_url else 'database'}"
    )

    # ✅ CREATE ENGINE (CLEAN MODERN VERSION)
    _engine = create_async_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_recycle=3600,
    )

    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
        autocommit=False,
    )

    logger.info("Database engine and session factory initialized successfully")


async def close_db() -> None:
    """Close database connections."""
    global _engine

    if _engine:
        logger.info("Closing database connections...")
        await _engine.dispose()
        _engine = None
        logger.info("Database connections closed")


def get_session_factory() -> async_sessionmaker:
    """Return session factory."""
    if _session_factory is None:
        raise RuntimeError("Database not initialized. Call init_db() first.")
    return _session_factory


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency-style async DB session.
    Usage:
        async with get_db_session() as session:
            ...
    """
    factory = get_session_factory()

    async with factory() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback()
            logger.error(f"Database session error: {e}")
            raise
        finally:
            await session.close()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Alias for compatibility."""
    async for session in get_db_session():
        yield session


class Database:
    """Database utility helpers."""

    @staticmethod
    async def health_check() -> bool:
        """Check DB connection."""
        if _engine is None:
            logger.error("Database engine not initialized")
            return False

        try:
            async with _engine.connect() as conn:
                await conn.execute(text("SELECT 1"))
                return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    @staticmethod
    async def create_all_tables() -> None:
        """Create tables from SQLAlchemy models."""
        if _engine is None:
            raise RuntimeError("Database not initialized")

        from app.models.models import Base

        logger.info("Creating database tables...")

        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

        logger.info("Database tables created successfully")

    @staticmethod
    async def drop_all_tables() -> None:
        """Drop all tables (dangerous)."""
        if _engine is None:
            raise RuntimeError("Database not initialized")

        from app.models.models import Base

        logger.warning("Dropping all database tables...")

        async with _engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

        logger.info("All tables dropped")
