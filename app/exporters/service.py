"""
Export System
Exports analyzed articles to JSON and CSV formats.
"""

import json
import csv
import logging
from pathlib import Path
from datetime import datetime
from typing import List, Optional
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Article, AISummary
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class ExportService:
    """Service for exporting articles and summaries."""

    def __init__(self, db_session: AsyncSession):
        """Initialize export service."""
        self.db = db_session
        self.settings = get_settings()
        self.export_path = Path(self.settings.export_path)
        self.export_path.mkdir(parents=True, exist_ok=True)

    async def export_all_articles(self, format_type: str = "json", limit: int = 1000) -> Path:
        """
        Export all articles with summaries.
        
        Args:
            format_type: 'json' or 'csv'
            limit: Maximum number of articles to export
            
        Returns:
            Path to exported file
        """
        logger.info(f"Exporting articles to {format_type}")
        
        # Fetch articles with summaries
        query = (
            select(Article, AISummary)
            .outerjoin(AISummary, Article.id == AISummary.article_id)
            .where(Article.is_processed == True)
            .order_by(desc(Article.published_at))
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        # Format data
        articles_data = []
        for article, summary in rows:
            article_dict = self._article_to_dict(article, summary)
            articles_data.append(article_dict)

        # Export based on format
        if format_type == "json":
            return await self._export_json(articles_data)
        elif format_type == "csv":
            return await self._export_csv(articles_data)
        else:
            raise ValueError(f"Unknown export format: {format_type}")

    async def _export_json(self, articles: List[dict]) -> Path:
        """Export articles to JSON."""
        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        filename = self.export_path / f"articles_{timestamp}.json"
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(
                {
                    "export_timestamp": datetime.utcnow().isoformat(),
                    "total_articles": len(articles),
                    "articles": articles,
                },
                f,
                indent=2,
                ensure_ascii=False,
                default=str
            )
        
        logger.info(f"Exported {len(articles)} articles to {filename}")
        return filename

    async def _export_csv(self, articles: List[dict]) -> Path:
        """Export articles to CSV."""
        timestamp = datetime.utcnow().isoformat().replace(":", "-")
        filename = self.export_path / f"articles_{timestamp}.csv"
        
        if not articles:
            logger.warning("No articles to export")
            return filename

        # Define CSV columns
        fieldnames = [
            "id", "title", "url", "author", "source_site",
            "published_at", "scraped_at",
            "summary", "sentiment", "hype_score", "trending_probability",
            "gamer_interest", "mentioned_games", "tags"
        ]

        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for article in articles:
                # Flatten nested data for CSV
                row = {
                    "id": article["id"],
                    "title": article["title"],
                    "url": article["url"],
                    "author": article.get("author", ""),
                    "source_site": article["source_site"],
                    "published_at": article["published_at"],
                    "scraped_at": article["scraped_at"],
                    "summary": article.get("summary", ""),
                    "sentiment": article.get("sentiment", ""),
                    "hype_score": article.get("hype_score", ""),
                    "trending_probability": article.get("trending_probability", ""),
                    "gamer_interest": article.get("gamer_interest", ""),
                    "mentioned_games": "|".join(article.get("mentioned_games", [])),
                    "tags": "|".join(article.get("tags", [])),
                }
                writer.writerow(row)

        logger.info(f"Exported {len(articles)} articles to {filename}")
        return filename

    async def export_by_sentiment(self, sentiment: str, format_type: str = "json") -> Path:
        """Export articles filtered by sentiment."""
        from app.models.models import SentimentType
        
        sentiment_enum = SentimentType(sentiment.lower())
        
        query = (
            select(Article, AISummary)
            .join(AISummary, Article.id == AISummary.article_id)
            .where(AISummary.sentiment == sentiment_enum)
            .order_by(desc(Article.published_at))
            .limit(1000)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        articles_data = [
            self._article_to_dict(article, summary)
            for article, summary in rows
        ]
        
        if format_type == "json":
            return await self._export_json(articles_data)
        else:
            return await self._export_csv(articles_data)

    async def export_trending(self, hours: int = 24, limit: int = 100) -> Path:
        """Export trending articles."""
        from datetime import timedelta
        
        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = (
            select(Article, AISummary)
            .outerjoin(AISummary, Article.id == AISummary.article_id)
            .where(Article.published_at >= cutoff_time)
            .order_by(desc(AISummary.hype_score) if AISummary.hype_score else desc(Article.published_at))
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        articles_data = [
            self._article_to_dict(article, summary)
            for article, summary in rows
        ]
        
        return await self._export_json(articles_data)

    @staticmethod
    def _article_to_dict(article: Article, summary: Optional[AISummary]) -> dict:
        """Convert article and summary to dictionary."""
        return {
            "id": article.id,
            "title": article.title,
            "url": article.url,
            "author": article.author,
            "source_site": article.source_site,
            "published_at": article.published_at.isoformat(),
            "scraped_at": article.scraped_at.isoformat(),
            "thumbnail_url": article.thumbnail_url,
            "tags": article.tags,
            "related_games": article.related_games,
            "summary": summary.summary if summary else None,
            "bullet_points": summary.bullet_points if summary else [],
            "sentiment": summary.sentiment.value if summary else None,
            "hype_score": summary.hype_score if summary else None,
            "category": summary.main_category if summary else None,
            "trending_probability": summary.trend_probability if summary else None,
            "gamer_interest": summary.gamer_interest if summary else None,
            "mentioned_games": summary.mentioned_games if summary else [],
            "ai_model": summary.ai_model_used if summary else None,
            "ai_provider": summary.ai_provider if summary else None,
        }
