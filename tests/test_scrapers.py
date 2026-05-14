"""
Tests for Scraper Components
"""

import pytest
from datetime import datetime
from app.scrapers.base import ArticleData, ScraperBase, RateLimiter


@pytest.mark.asyncio
async def test_article_data_hash():
    """Test article content hash calculation."""
    article = ArticleData(
        title="Test Article",
        url="https://example.com/test",
        author="Test Author",
        body="This is test content",
        published_at=datetime.utcnow(),
        thumbnail_url=None,
        tags=["test"],
    )
    
    hash1 = article.calculate_content_hash()
    assert hash1 is not None
    assert len(hash1) == 64  # SHA256 hex string length
    
    # Same content should produce same hash
    article2 = ArticleData(
        title="Test Article",
        url="https://example.com/test2",
        author="Test Author",
        body="This is test content",
        published_at=datetime.utcnow(),
        thumbnail_url=None,
        tags=["test"],
    )
    hash2 = article2.calculate_content_hash()
    assert hash1 == hash2


@pytest.mark.asyncio
async def test_rate_limiter():
    """Test rate limiter functionality."""
    limiter = RateLimiter(max_requests_per_second=2.0)
    
    # First wait should be instant
    import time
    start = time.time()
    await limiter.wait()
    elapsed = time.time() - start
    assert elapsed < 0.1
    
    # Subsequent waits should respect rate limit
    start = time.time()
    await limiter.wait()
    elapsed = time.time() - start
    # Should wait ~0.5 seconds for 2 req/sec
    assert 0.4 < elapsed < 0.7


@pytest.mark.asyncio
async def test_scraper_url_normalization():
    """Test URL normalization."""
    base_url = "https://example.com"
    
    # Absolute URL
    normalized = ScraperBase.normalize_url("https://example.com/article/123", base_url)
    assert normalized == "https://example.com/article/123"
    
    # Relative URL
    normalized = ScraperBase.normalize_url("/article/123", base_url)
    assert normalized == "https://example.com/article/123"
    
    # URL with query params (should keep path only)
    url = "https://example.com/article/123?utm_source=test"
    normalized = ScraperBase.normalize_url(url)
    assert normalized == "https://example.com/article/123"


@pytest.mark.asyncio
async def test_scraper_html_cleaning():
    """Test HTML content cleaning."""
    html = """
    <html>
        <script>alert('test')</script>
        <p>Article content here</p>
        <nav>Navigation</nav>
        <footer>Footer content</footer>
    </html>
    """
    
    cleaned = ScraperBase.clean_html(html)
    assert "Article content here" in cleaned
    assert "alert" not in cleaned
    assert "Navigation" not in cleaned
    assert "Footer content" not in cleaned
