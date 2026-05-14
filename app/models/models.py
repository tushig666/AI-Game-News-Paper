"""
Database Models
SQLAlchemy 2.0 ORM models for game news articles and AI analysis.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    Column, String, Text, DateTime, Integer, Float, Boolean,
    Index, ForeignKey, Enum, JSON
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import enum

Base = declarative_base()


class SentimentType(str, enum.Enum):
    """Sentiment classification enum."""
    BULLISH = "bullish"
    BEARISH = "bearish"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class ArticleCategory(str, enum.Enum):
    """Article category enum."""
    NEWS = "news"
    REVIEW = "review"
    FEATURE = "feature"
    INTERVIEW = "interview"
    RUMOR = "rumor"
    UPDATE = "update"
    OTHER = "other"


class Article(Base):
    """
    Core article model representing a scraped game news article.
    
    Stores:
    - Article metadata (title, URL, author, publication date)
    - Content (body, tags, related games)
    - Scraping metadata (source, scraped_at)
    """
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True, index=True)
    
    # Core Content
    title = Column(String(512), nullable=False, index=True)
    url = Column(String(2048), nullable=False, unique=True, index=True)
    author = Column(String(255), nullable=True)
    body = Column(Text, nullable=False)
    summary_short = Column(String(500), nullable=True)
    
    # Metadata
    published_at = Column(DateTime, nullable=False, index=True)
    scraped_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Content Attributes
    thumbnail_url = Column(String(2048), nullable=True)
    tags = Column(JSON, default=list, nullable=False)
    related_games = Column(JSON, default=list, nullable=False)
    category = Column(Enum(ArticleCategory), default=ArticleCategory.NEWS)
    
    # Source Information
    source_site = Column(String(100), nullable=False, index=True)
    source_id = Column(String(255), nullable=True)  # Original article ID from source
    
    # Processing State
    is_duplicate = Column(Boolean, default=False, index=True)
    is_processed = Column(Boolean, default=False, index=True)
    content_hash = Column(String(64), unique=True, nullable=True)  # SHA256 of content
    
    # Relationships
    ai_summary = relationship("AISummary", back_populates="article", uselist=False, cascade="all, delete-orphan")
    scraping_logs = relationship("ScrapingLog", back_populates="article", cascade="all, delete-orphan")
    
    # Indexes
    __table_args__ = (
        Index("idx_article_source_published", "source_site", "published_at"),
        Index("idx_article_processed", "is_processed", "published_at"),
        Index("idx_article_duplicate", "is_duplicate"),
    )

    def __repr__(self) -> str:
        return f"<Article(id={self.id}, title={self.title[:50]}..., source={self.source_site})>"


class AISummary(Base):
    """
    AI-generated analysis and summary of articles.
    
    Stores:
    - LLM-generated summaries and key points
    - Sentiment analysis
    - Hype scores and trend predictions
    - Gamer interest metrics
    """
    __tablename__ = "ai_summaries"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=False, unique=True, index=True)
    
    # Summary Content
    summary = Column(Text, nullable=False)
    bullet_points = Column(JSON, default=list, nullable=False)
    
    # Analysis Results
    sentiment = Column(Enum(SentimentType), nullable=False)
    hype_score = Column(Integer, nullable=False)  # 0-100
    trend_probability = Column(Float, nullable=False)  # 0.0-1.0
    gamer_interest = Column(Integer, nullable=False)  # 0-100
    
    # Categorization
    main_category = Column(String(100), nullable=False)
    sub_categories = Column(JSON, default=list, nullable=False)
    
    # Key Entities
    mentioned_games = Column(JSON, default=list, nullable=False)
    mentioned_developers = Column(JSON, default=list, nullable=False)
    mentioned_publishers = Column(JSON, default=list, nullable=False)
    
    # Token Usage & Cost
    input_tokens = Column(Integer, nullable=False)
    output_tokens = Column(Integer, nullable=False)
    estimated_cost = Column(Float, nullable=False)
    
    # Metadata
    ai_model_used = Column(String(100), nullable=False)
    ai_provider = Column(String(50), nullable=False)
    processing_time_ms = Column(Integer, nullable=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    article = relationship("Article", back_populates="ai_summary")
    
    __table_args__ = (
        Index("idx_summary_sentiment", "sentiment"),
        Index("idx_summary_hype_score", "hype_score"),
        Index("idx_summary_trend_probability", "trend_probability"),
    )

    def __repr__(self) -> str:
        return f"<AISummary(id={self.id}, article_id={self.article_id}, sentiment={self.sentiment})>"


class SourceSite(Base):
    """
    Metadata about scraping sources.
    
    Tracks:
    - Source configuration
    - Last scrape time
    - Success/failure rates
    """
    __tablename__ = "source_sites"

    id = Column(Integer, primary_key=True, index=True)
    
    # Site Information
    name = Column(String(100), nullable=False, unique=True, index=True)
    url = Column(String(512), nullable=False)
    description = Column(Text, nullable=True)
    
    # Scraping Configuration
    is_active = Column(Boolean, default=True, index=True)
    scraper_type = Column(String(50), nullable=False)  # e.g., 'playwright', 'beautifulsoup'
    articles_selector = Column(String(255), nullable=True)
    
    # Statistics
    total_articles_scraped = Column(Integer, default=0)
    last_scraped_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    success_rate = Column(Float, default=100.0)  # Percentage
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<SourceSite(id={self.id}, name={self.name})>"


class ScrapingLog(Base):
    """
    Detailed scraping activity log.
    
    Tracks:
    - Individual scraping attempts
    - Success/failure status
    - Error information
    - Performance metrics
    """
    __tablename__ = "scraping_logs"

    id = Column(Integer, primary_key=True, index=True)
    article_id = Column(Integer, ForeignKey("articles.id"), nullable=True)
    
    # Log Information
    source_site = Column(String(100), nullable=False, index=True)
    status = Column(String(50), nullable=False)  # 'success', 'failed', 'timeout', 'retry'
    error_message = Column(Text, nullable=True)
    
    # Performance
    duration_ms = Column(Integer, nullable=False)
    http_status_code = Column(Integer, nullable=True)
    
    # Metadata
    url_scraped = Column(String(2048), nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    # Relationships
    article = relationship("Article", back_populates="scraping_logs")
    
    __table_args__ = (
        Index("idx_scraping_log_source_status", "source_site", "status"),
        Index("idx_scraping_log_timestamp", "timestamp"),
    )

    def __repr__(self) -> str:
        return f"<ScrapingLog(id={self.id}, source={self.source_site}, status={self.status})>"


class TrendingScore(Base):
    """
    Time-based trending score calculations.
    
    Tracks:
    - Hype trends over time
    - Sentiment trends
    - Velocity metrics
    """
    __tablename__ = "trending_scores"

    id = Column(Integer, primary_key=True, index=True)
    
    # Entity Being Tracked
    game_title = Column(String(256), nullable=False, index=True)
    
    # Trend Metrics
    average_hype_score = Column(Float, nullable=False)
    dominant_sentiment = Column(Enum(SentimentType), nullable=False)
    article_count_24h = Column(Integer, default=0)
    article_count_7d = Column(Integer, default=0)
    
    # Velocity
    hype_velocity = Column(Float, nullable=False)  # Change rate
    sentiment_shift = Column(String(50), nullable=True)  # "improving", "declining", "stable"
    
    # Prediction
    trending_probability = Column(Float, nullable=False)  # 0.0-1.0
    predicted_peak_at = Column(DateTime, nullable=True)
    
    # Metadata
    calculated_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_trending_game_title", "game_title"),
        Index("idx_trending_probability", "trending_probability"),
    )

    def __repr__(self) -> str:
        return f"<TrendingScore(id={self.id}, game={self.game_title}, hype={self.average_hype_score})>"
