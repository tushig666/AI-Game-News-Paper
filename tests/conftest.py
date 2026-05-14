"""
Test Configuration and Fixtures
"""

import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from app.models.models import Base


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator[AsyncSession, None]:
    """Create test database session."""
    # Use in-memory SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False,
        future=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    async with SessionLocal() as session:
        yield session

    await engine.dispose()


@pytest.fixture
def sample_article_data():
    """Sample article data for testing."""
    from datetime import datetime
    return {
        "title": "Test Gaming Article",
        "url": "https://example.com/test-article",
        "body": "This is a test article about game news " * 10,
        "author": "Test Author",
        "published_at": datetime.utcnow(),
        "source_site": "TestSite",
        "thumbnail_url": "https://example.com/thumb.jpg",
        "tags": ["test", "gaming"],
    }


@pytest.fixture
def sample_summary_data():
    """Sample AI summary data for testing."""
    return {
        "summary": "Test game announcement with major implications",
        "bullet_points": [
            "Major studio announcement",
            "New IP revealed",
            "Release date confirmed"
        ],
        "sentiment": "bullish",
        "hype_score": 85,
        "category": "news",
        "trending_probability": 0.75,
        "gamer_interest": 90,
    }
