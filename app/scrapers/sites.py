"""
Concrete Scraper Implementations
Site-specific scrapers for major gaming news websites.
"""

import logging
from datetime import datetime, timedelta
from typing import List, Optional
from bs4 import BeautifulSoup
from app.scrapers.base import ScraperBase, ArticleData, RateLimiter

logger = logging.getLogger(__name__)


class IGNScraper(ScraperBase):
    """Scraper for IGN.com gaming news."""

    def __init__(self):
        super().__init__(
            site_name="IGN",
            base_url="https://www.ign.com",
            timeout=30
        )
        self.rate_limiter = RateLimiter(max_requests_per_second=0.5)

    async def scrape(self) -> List[ArticleData]:
        """Scrape IGN gaming news."""
        articles = []
        url = "https://www.ign.com/games"

        await self.rate_limiter.wait()
        html = await self.fetch_page(url)
        
        if not html:
            return articles

        soup = BeautifulSoup(html, 'html.parser')
        
        # IGN uses article elements
        article_elements = soup.find_all('article', limit=20)

        for element in article_elements:
            try:
                title_elem = element.find('a', class_='title')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                article_url = title_elem.get('href', '')
                article_url = self.normalize_url(article_url, self.base_url)

                # Extract other metadata
                author_elem = element.find('span', class_='author')
                author = author_elem.get_text(strip=True) if author_elem else None

                time_elem = element.find('span', class_='publish-time')
                published_at = datetime.utcnow() if not time_elem else datetime.utcnow()

                desc_elem = element.find('p', class_='description')
                body = desc_elem.get_text(strip=True) if desc_elem else title

                thumb_elem = element.find('img')
                thumbnail_url = thumb_elem.get('src', '') if thumb_elem else None

                articles.append(ArticleData(
                    title=title,
                    url=article_url,
                    author=author,
                    body=body,
                    published_at=published_at,
                    thumbnail_url=thumbnail_url,
                    tags=["gaming", "news"],
                    source_id=f"ign_{len(articles)}"
                ))

            except Exception as e:
                logger.warning(f"Error parsing IGN article: {str(e)}")

        logger.info(f"Scraped {len(articles)} articles from IGN")
        return articles


class GameSpotScraper(ScraperBase):
    """Scraper for GameSpot.com gaming news."""

    def __init__(self):
        super().__init__(
            site_name="GameSpot",
            base_url="https://www.gamespot.com",
            timeout=30
        )
        self.rate_limiter = RateLimiter(max_requests_per_second=0.5)

    async def scrape(self) -> List[ArticleData]:
        """Scrape GameSpot gaming news."""
        articles = []
        url = "https://www.gamespot.com/news/"

        await self.rate_limiter.wait()
        html = await self.fetch_page(url)
        
        if not html:
            return articles

        soup = BeautifulSoup(html, 'html.parser')
        
        # GameSpot uses div.gs-item
        article_elements = soup.find_all('div', class_='gs-item', limit=20)

        for element in article_elements:
            try:
                title_elem = element.find('a', class_='gs-title')
                if not title_elem:
                    title_elem = element.find('a')
                    
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                article_url = title_elem.get('href', '')
                article_url = self.normalize_url(article_url, self.base_url)

                body_elem = element.find('p', class_='gs-description')
                body = body_elem.get_text(strip=True) if body_elem else title

                articles.append(ArticleData(
                    title=title,
                    url=article_url,
                    author=None,
                    body=body,
                    published_at=datetime.utcnow(),
                    thumbnail_url=None,
                    tags=["gaming", "gamespot"],
                    source_id=f"gamespot_{len(articles)}"
                ))

            except Exception as e:
                logger.warning(f"Error parsing GameSpot article: {str(e)}")

        logger.info(f"Scraped {len(articles)} articles from GameSpot")
        return articles


class PCGamerScraper(ScraperBase):
    """Scraper for PCGamer.com gaming news."""

    def __init__(self):
        super().__init__(
            site_name="PC Gamer",
            base_url="https://www.pcgamer.com",
            timeout=30
        )
        self.rate_limiter = RateLimiter(max_requests_per_second=0.5)

    async def scrape(self) -> List[ArticleData]:
        """Scrape PC Gamer news."""
        articles = []
        url = "https://www.pcgamer.com/news/"

        await self.rate_limiter.wait()
        html = await self.fetch_page(url)
        
        if not html:
            return articles

        soup = BeautifulSoup(html, 'html.parser')
        
        article_elements = soup.find_all('article', limit=20)

        for element in article_elements:
            try:
                title_elem = element.find('a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                article_url = title_elem.get('href', '')
                article_url = self.normalize_url(article_url, self.base_url)

                body_elem = element.find('p')
                body = body_elem.get_text(strip=True) if body_elem else title

                articles.append(ArticleData(
                    title=title,
                    url=article_url,
                    author=None,
                    body=body,
                    published_at=datetime.utcnow(),
                    thumbnail_url=None,
                    tags=["pc", "gaming"],
                    source_id=f"pcgamer_{len(articles)}"
                ))

            except Exception as e:
                logger.warning(f"Error parsing PC Gamer article: {str(e)}")

        logger.info(f"Scraped {len(articles)} articles from PC Gamer")
        return articles


class PolygonScraper(ScraperBase):
    """Scraper for Polygon.com gaming coverage."""

    def __init__(self):
        super().__init__(
            site_name="Polygon",
            base_url="https://www.polygon.com",
            timeout=30
        )
        self.rate_limiter = RateLimiter(max_requests_per_second=0.5)

    async def scrape(self) -> List[ArticleData]:
        """Scrape Polygon gaming content."""
        articles = []
        url = "https://www.polygon.com/games"

        await self.rate_limiter.wait()
        html = await self.fetch_page(url)
        
        if not html:
            return articles

        soup = BeautifulSoup(html, 'html.parser')
        
        article_elements = soup.find_all('div', class_='c-entry-box', limit=20)

        for element in article_elements:
            try:
                title_elem = element.find('a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                article_url = title_elem.get('href', '')
                article_url = self.normalize_url(article_url, self.base_url)

                articles.append(ArticleData(
                    title=title,
                    url=article_url,
                    author=None,
                    body=title,
                    published_at=datetime.utcnow(),
                    thumbnail_url=None,
                    tags=["polygon", "games"],
                    source_id=f"polygon_{len(articles)}"
                ))

            except Exception as e:
                logger.warning(f"Error parsing Polygon article: {str(e)}")

        logger.info(f"Scraped {len(articles)} articles from Polygon")
        return articles


class EurogamerScraper(ScraperBase):
    """Scraper for Eurogamer.net gaming news."""

    def __init__(self):
        super().__init__(
            site_name="Eurogamer",
            base_url="https://www.eurogamer.net",
            timeout=30
        )
        self.rate_limiter = RateLimiter(max_requests_per_second=0.5)

    async def scrape(self) -> List[ArticleData]:
        """Scrape Eurogamer news."""
        articles = []
        url = "https://www.eurogamer.net/"

        await self.rate_limiter.wait()
        html = await self.fetch_page(url)
        
        if not html:
            return articles

        soup = BeautifulSoup(html, 'html.parser')
        
        article_elements = soup.find_all('article', limit=20)

        for element in article_elements:
            try:
                title_elem = element.find('a')
                if not title_elem:
                    continue

                title = title_elem.get_text(strip=True)
                article_url = title_elem.get('href', '')
                article_url = self.normalize_url(article_url, self.base_url)

                articles.append(ArticleData(
                    title=title,
                    url=article_url,
                    author=None,
                    body=title,
                    published_at=datetime.utcnow(),
                    thumbnail_url=None,
                    tags=["eurogamer"],
                    source_id=f"eurogamer_{len(articles)}"
                ))

            except Exception as e:
                logger.warning(f"Error parsing Eurogamer article: {str(e)}")

        logger.info(f"Scraped {len(articles)} articles from Eurogamer")
        return articles


def get_all_scrapers() -> List[ScraperBase]:
    """Get list of all active scrapers."""
    return [
        IGNScraper(),
        GameSpotScraper(),
        PCGamerScraper(),
        PolygonScraper(),
        EurogamerScraper(),
    ]
