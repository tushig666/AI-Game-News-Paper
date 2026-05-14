"""
Web Scraper Base Classes and Utilities
Foundation for multi-site scraping with async support.
"""

import asyncio
import logging
import random
import hashlib
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any
from datetime import datetime
from dataclasses import dataclass
import aiohttp
from bs4 import BeautifulSoup
import html

logger = logging.getLogger(__name__)


USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
]


@dataclass
class ArticleData:
    """Scraped article data structure."""
    title: str
    url: str
    author: Optional[str]
    body: str
    published_at: datetime
    thumbnail_url: Optional[str]
    tags: List[str]
    category: str = "news"
    source_id: Optional[str] = None

    def calculate_content_hash(self) -> str:
        """Calculate SHA256 hash of article content."""
        content = f"{self.title}{self.body}".encode('utf-8')
        return hashlib.sha256(content).hexdigest()


class ScraperBase(ABC):
    """
    Abstract base class for website scrapers.
    
    Each concrete scraper implements:
    - site-specific article extraction
    - URL normalization
    - content cleaning
    - rate limiting
    """

    def __init__(
        self,
        site_name: str,
        base_url: str,
        timeout: int = 30,
        retry_attempts: int = 3,
    ):
        """
        Initialize scraper.
        
        Args:
            site_name: Name of the website (e.g., 'IGN', 'GameSpot')
            base_url: Base URL of website
            timeout: Request timeout in seconds
            retry_attempts: Number of retry attempts
        """
        self.site_name = site_name
        self.base_url = base_url
        self.timeout = timeout
        self.retry_attempts = retry_attempts
        self.session: Optional[aiohttp.ClientSession] = None

    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()

    async def fetch_page(self, url: str) -> Optional[str]:
        """
        Fetch page content with retries and error handling.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use 'async with' context manager.")

        for attempt in range(self.retry_attempts):
            try:
                headers = {"User-Agent": random.choice(USER_AGENTS)}
                
                async with self.session.get(
                    url,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=self.timeout),
                    ssl=False
                ) as resp:
                    if resp.status == 200:
                        return await resp.text()
                    elif resp.status == 429:  # Rate limited
                        wait_time = 2 ** attempt
                        logger.warning(f"Rate limited. Waiting {wait_time}s before retry...")
                        await asyncio.sleep(wait_time)
                    else:
                        logger.warning(f"HTTP {resp.status} for {url}")
                        
            except asyncio.TimeoutError:
                logger.warning(f"Timeout fetching {url} (attempt {attempt + 1}/{self.retry_attempts})")
            except Exception as e:
                logger.error(f"Error fetching {url}: {str(e)}")

        logger.error(f"Failed to fetch {url} after {self.retry_attempts} attempts")
        return None

    @abstractmethod
    async def scrape(self) -> List[ArticleData]:
        """
        Scrape articles from the website.
        Must be implemented by concrete scrapers.
        
        Returns:
            List of scraped articles
        """
        pass

    @staticmethod
    def clean_html(html_text: str) -> str:
        """
        Clean and normalize HTML content.
        
        Args:
            html_text: Raw HTML content
            
        Returns:
            Cleaned text
        """
        # Remove script and style elements
        soup = BeautifulSoup(html_text, 'html.parser')
        for script in soup(["script", "style", "nav", "footer"]):
            script.decompose()

        # Get text
        text = soup.get_text()

        # Clean up whitespace
        lines = (line.strip() for line in text.splitlines())
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        text = ' '.join(chunk for chunk in chunks if chunk)

        return html.unescape(text)

    @staticmethod
    def normalize_url(url: str, base_url: Optional[str] = None) -> str:
        """
        Normalize URL (remove query params, anchors, etc.).
        
        Args:
            url: URL to normalize
            base_url: Base URL for relative URLs
            
        Returns:
            Normalized URL
        """
        from urllib.parse import urlparse, urljoin

        if base_url and not url.startswith(('http://', 'https://')):
            url = urljoin(base_url, url)

        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"


class RateLimiter:
    """
    Rate limiter for controlling scraping speed.
    Prevents overwhelming target servers.
    """

    def __init__(self, max_requests_per_second: float = 1.0):
        """
        Initialize rate limiter.
        
        Args:
            max_requests_per_second: Maximum requests per second
        """
        self.max_requests_per_second = max_requests_per_second
        self.min_interval = 1.0 / max_requests_per_second
        self.last_request_time: Optional[float] = None

    async def wait(self) -> None:
        """Wait if necessary to maintain rate limit."""
        import time
        
        if self.last_request_time is None:
            self.last_request_time = time.time()
            return

        elapsed = time.time() - self.last_request_time
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)

        self.last_request_time = time.time()


class ScraperPool:
    """
    Manages a pool of scraper workers for concurrent scraping.
    """

    def __init__(self, scrapers: List[ScraperBase], max_concurrent: int = 4):
        """
        Initialize scraper pool.
        
        Args:
            scrapers: List of scraper instances
            max_concurrent: Maximum concurrent scrapers
        """
        self.scrapers = scrapers
        self.max_concurrent = max_concurrent
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def scrape_all(self) -> Dict[str, List[ArticleData]]:
        """
        Scrape all sources concurrently with semaphore control.
        
        Returns:
            Dictionary mapping site names to articles
        """
        tasks = [
            self._scrape_with_semaphore(scraper)
            for scraper in self.scrapers
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        output = {}
        for scraper, result in zip(self.scrapers, results):
            if isinstance(result, Exception):
                logger.error(f"Scraper error for {scraper.site_name}: {str(result)}")
                output[scraper.site_name] = []
            else:
                output[scraper.site_name] = result

        return output

    async def _scrape_with_semaphore(self, scraper: ScraperBase) -> List[ArticleData]:
        """Scrape with semaphore control."""
        async with self.semaphore:
            logger.info(f"Starting scrape of {scraper.site_name}")
            async with scraper:
                return await scraper.scrape()
