"""
Article Service Layer
Core business logic for article processing and analysis.
"""

import logging
import json
from typing import Optional, List
from datetime import datetime
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.models import Article, AISummary, SentimentType, ArticleCategory
from app.ai.service import AIServiceFactory, AIResponse
from app.config.settings import get_settings

logger = logging.getLogger(__name__)


class ArticleService:
    """Service for managing articles in the database."""

    def __init__(self, db_session: AsyncSession):
        """Initialize article service with database session."""
        self.db = db_session

    async def article_exists(self, url: str) -> bool:
        """Check if article with URL already exists."""
        query = select(func.count()).select_from(Article).where(Article.url == url)
        result = await self.db.execute(query)
        count = result.scalar()
        return count > 0

    async def get_by_url(self, url: str) -> Optional[Article]:
        """Get article by URL."""
        query = select(Article).where(Article.url == url)
        result = await self.db.execute(query)
        return result.scalars().first()

    async def create_article(
        self,
        title: str,
        url: str,
        body: str,
        published_at: datetime,
        source_site: str,
        author: Optional[str] = None,
        thumbnail_url: Optional[str] = None,
        tags: Optional[List[str]] = None,
        related_games: Optional[List[str]] = None,
        category: str = "news",
        source_id: Optional[str] = None,
    ) -> Article:
        """Create new article."""
        article = Article(
            title=title,
            url=url,
            author=author,
            body=body,
            published_at=published_at,
            source_site=source_site,
            thumbnail_url=thumbnail_url,
            tags=tags or [],
            related_games=related_games or [],
            category=category,
            source_id=source_id,
        )
        
        self.db.add(article)
        await self.db.flush()  # Get ID without committing
        
        logger.debug(f"Created article: {article.id} - {title[:50]}")
        return article

    async def get_unprocessed_articles(self, limit: int = 50) -> List[Article]:
        """Get unprocessed articles."""
        query = (
            select(Article)
            .where(Article.is_processed == False)
            .order_by(Article.published_at.desc())
            .limit(limit)
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    async def mark_as_processed(self, article_id: int) -> None:
        """Mark article as processed."""
        article = await self.db.get(Article, article_id)
        if article:
            article.is_processed = True


class SummarizationService:
    """Service for AI summarization of articles."""

    def __init__(self, db_session: AsyncSession):
        """Initialize summarization service."""
        self.db = db_session
        self.settings = get_settings()

    async def summarize_article(self, article: Article) -> Optional[AISummary]:
        """
        Summarize article using AI.
        
        Args:
            article: Article to summarize
            
        Returns:
            AISummary object or None if failed
        """
        if not article.body or len(article.body.strip()) < 100:
            logger.warning(f"Article {article.id} too short for summarization")
            return None

        try:
            ai_service = AIServiceFactory.create_service()
            
            async with ai_service as service:
                response = await service.summarize_article(article.body)

            # Parse JSON response
            import json
            analysis = json.loads(response.content)

            # Create AI summary record
            summary = AISummary(
                article_id=article.id,
                summary=analysis.get("summary", ""),
                bullet_points=analysis.get("bullet_points", []),
                sentiment=SentimentType(analysis.get("sentiment", "neutral")),
                hype_score=int(analysis.get("hype_score", 50)),
                trend_probability=float(analysis.get("trending_probability", 0.5)) / 100.0,
                gamer_interest=int(analysis.get("gamer_interest", 50)),
                main_category=analysis.get("category", "news"),
                sub_categories=[],
                mentioned_games=article.related_games,
                mentioned_developers=[],
                mentioned_publishers=[],
                input_tokens=response.input_tokens,
                output_tokens=response.output_tokens,
                estimated_cost=self._calculate_cost(
                    response.input_tokens,
                    response.output_tokens,
                    response.provider
                ),
                ai_model_used=response.model_used,
                ai_provider=response.provider,
                processing_time_ms=0,
            )

            self.db.add(summary)
            logger.info(f"Summarized article {article.id}: sentiment={summary.sentiment.value}, hype={summary.hype_score}")
            
            return summary

        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse AI response for article {article.id}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Summarization failed for article {article.id}: {str(e)}")
            return None

    @staticmethod
    def _calculate_cost(
        input_tokens: int,
        output_tokens: int,
        provider: str
    ) -> float:
        """
        Calculate estimated API cost.
        
        Pricing (as of 2024):
        - Claude 3.5 Sonnet: $3/1M input, $15/1M output
        - GPT-4 Turbo: $10/1M input, $30/1M output
        """
        if provider == "anthropic":
            input_cost = (input_tokens / 1_000_000) * 3
            output_cost = (output_tokens / 1_000_000) * 15
        elif provider == "openai":
            input_cost = (input_tokens / 1_000_000) * 10
            output_cost = (output_tokens / 1_000_000) * 30
        else:
            input_cost = output_cost = 0

        return round(input_cost + output_cost, 6)


class DuplicateDetectionService:
    """Service for detecting duplicate articles."""

    def __init__(self, db_session: AsyncSession):
        """Initialize duplicate detection service."""
        self.db = db_session

    async def check_duplicate(self, article: Article) -> bool:
        """
        Check if article is a duplicate based on content hash.
        
        Args:
            article: Article to check
            
        Returns:
            True if duplicate, False otherwise
        """
        content_hash = article.content_hash or self._calculate_hash(article.body)
        
        query = select(func.count()).select_from(Article).where(
            Article.content_hash == content_hash,
            Article.id != article.id
        )
        result = await self.db.execute(query)
        count = result.scalar()
        
        if count > 0:
            article.is_duplicate = True
            logger.info(f"Duplicate detected for article {article.id}")
            return True

        article.content_hash = content_hash
        return False

    @staticmethod
    def _calculate_hash(content: str) -> str:
        """Calculate SHA256 hash of content."""
        import hashlib
        return hashlib.sha256(content.encode('utf-8')).hexdigest()


class AnalyticsService:
    """Service for analytics and trending calculations."""

    def __init__(self, db_session: AsyncSession):
        """Initialize analytics service."""
        self.db = db_session

    async def get_trending_games(self, hours: int = 24, limit: int = 10) -> List[dict]:
        """
        Get trending games based on recent articles.
        
        Args:
            hours: Look back period in hours
            limit: Maximum number of games to return
            
        Returns:
            List of trending game info
        """
        from datetime import timedelta
        from sqlalchemy import and_

        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = (
            select(
                Article.related_games,
                func.count(Article.id).label("article_count"),
                func.avg(AISummary.hype_score).label("avg_hype"),
            )
            .outerjoin(AISummary, Article.id == AISummary.article_id)
            .where(Article.published_at >= cutoff_time)
            .group_by(Article.related_games)
            .order_by(func.count(Article.id).desc())
            .limit(limit)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        trending = []
        for games, count, avg_hype in rows:
            if games:
                for game in games:
                    trending.append({
                        "game": game,
                        "article_count": count,
                        "average_hype": float(avg_hype) if avg_hype else 0,
                    })

        return trending

    async def get_sentiment_distribution(self, hours: int = 24) -> dict:
        """Get distribution of sentiments across articles."""
        from datetime import timedelta

        cutoff_time = datetime.utcnow() - timedelta(hours=hours)
        
        query = (
            select(
                AISummary.sentiment,
                func.count(AISummary.id).label("count")
            )
            .join(Article, AISummary.article_id == Article.id)
            .where(Article.published_at >= cutoff_time)
            .group_by(AISummary.sentiment)
        )
        
        result = await self.db.execute(query)
        rows = result.all()
        
        distribution = {sentiment.value: 0 for sentiment in SentimentType}
        for sentiment, count in rows:
            distribution[sentiment.value] = count

        return distribution
