"""
Configuration Management
Handles environment variables and application settings using pydantic-settings.
"""

from typing import Literal
from pydantic_settings import BaseSettings
from pydantic import Field, validator


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Database Configuration
    database_url: str = Field(
        default="postgresql+asyncpg://user:password@localhost:5432/game_news_ai",
        description="PostgreSQL async connection string"
    )
    database_pool_size: int = Field(default=20, description="Database connection pool size")
    database_max_overflow: int = Field(default=10, description="Database connection overflow")

    # API Keys
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")
    claude_api_key: str | None = Field(default=None, description="Claude API key (legacy)")
    anthropic_api_key: str | None = Field(default=None, description="Anthropic API key")

    # AI Configuration
    ai_provider: Literal["claude", "openai"] = Field(
        default="claude",
        description="Primary AI provider"
    )
    ai_model_summarize: str = Field(
        default="claude-3-5-sonnet-20241022",
        description="Model for summarization"
    )
    ai_model_fallback: str = Field(
        default="gpt-4-turbo",
        description="Fallback AI model"
    )
    ai_timeout_seconds: int = Field(default=60, description="AI API timeout")
    ai_retries: int = Field(default=3, description="AI API retry attempts")
    ai_backoff_factor: float = Field(default=1.5, description="Exponential backoff multiplier")

    # Scraping Configuration
    scraper_concurrent_workers: int = Field(default=4, description="Concurrent scraper workers")
    scraper_timeout_seconds: int = Field(default=30, description="Scraper timeout per page")
    scraper_retry_attempts: int = Field(default=3, description="Scraper retry attempts")
    scraper_retry_backoff: float = Field(default=2.0, description="Scraper retry backoff")
    scraper_request_timeout: int = Field(default=15, description="HTTP request timeout")
    scraper_user_agents_count: int = Field(default=5, description="User-Agent rotation pool size")
    scraping_interval_minutes: int = Field(default=30, description="Scraping interval in minutes")

    # Rate Limiting
    rate_limit_per_second: float = Field(default=2, description="Global rate limit per second")
    rate_limit_per_site: float = Field(default=1, description="Per-site rate limit per second")

    # Logging
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = Field(
        default="INFO",
        description="Logging level"
    )
    log_file: str = Field(default="logs/app.log", description="Log file path")
    log_max_bytes: int = Field(default=10485760, description="Max log file size (bytes)")
    log_backup_count: int = Field(default=5, description="Number of backup log files")

    # Environment
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        description="Deployment environment"
    )
    debug: bool = Field(default=True, description="Debug mode")
    host: str = Field(default="0.0.0.0", description="Application host")
    port: int = Field(default=8000, description="Application port")

    # Services
    enable_health_check: bool = Field(default=True, description="Enable health checks")
    enable_metrics: bool = Field(default=True, description="Enable metrics collection")
    enable_caching: bool = Field(default=True, description="Enable caching layer")

    # Export Configuration
    export_format: Literal["json", "csv", "both"] = Field(default="json", description="Export format")
    export_path: str = Field(default="./exports", description="Export directory path")
    export_batch_size: int = Field(default=50, description="Export batch size")

    # Redis Cache
    redis_url: str | None = Field(default="redis://localhost:6379/0", description="Redis connection URL")
    cache_ttl_seconds: int = Field(default=3600, description="Cache TTL in seconds")

    # Monitoring
    sentry_dsn: str | None = Field(default=None, description="Sentry error tracking DSN")
    enable_sentry: bool = Field(default=False, description="Enable Sentry error tracking")

    # Feature Flags
    feature_duplicate_detection: bool = Field(default=True, description="Enable duplicate detection")
    feature_sentiment_analysis: bool = Field(default=True, description="Enable sentiment analysis")
    feature_trend_prediction: bool = Field(default=True, description="Enable trend prediction")

    @validator("database_pool_size", "database_max_overflow")
    def validate_pool_size(cls, v):
        """Validate pool sizes are positive."""
        if v <= 0:
            raise ValueError("Pool size must be positive")
        return v

    @validator("ai_retries", "scraper_retry_attempts")
    def validate_retries(cls, v):
        """Validate retry attempts are reasonable."""
        if not (1 <= v <= 10):
            raise ValueError("Retries must be between 1 and 10")
        return v

    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.environment == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.environment == "development"


def get_settings() -> Settings:
    """Get application settings singleton."""
    return Settings()
