"""Game News AI Platform - Async CLI Tools"""

import asyncio
import logging
import sys
from datetime import datetime

from app.config.settings import get_settings
from app.database.connection import init_db, close_db, Database, get_session_factory
from app.utils.logging_config import setup_logging, get_logger
from app.pipelines.processing import run_pipeline_once
from app.services.article import AnalyticsService
from app.exporters.service import ExportService

logger = get_logger(__name__)


async def cmd_scrape() -> None:
    """Run one scraping cycle."""
    setup_logging()
    await init_db()
    try:
        logger.info("Running single scrape cycle...")
        stats = await run_pipeline_once()
        logger.info(f"Scrape complete: {stats}")
    finally:
        await close_db()


async def cmd_export(format_type: str = "json", limit: int = 1000) -> None:
    """Export articles to file."""
    setup_logging()
    await init_db()
    try:
        session_factory = get_session_factory()
        async with session_factory() as db:
            export_service = ExportService(db)
            filepath = await export_service.export_all_articles(format_type, limit)
            logger.info(f"Exported to: {filepath}")
    finally:
        await close_db()


async def cmd_trending(hours: int = 24) -> None:
    """Show trending games."""
    setup_logging()
    await init_db()
    try:
        session_factory = get_session_factory()
        async with session_factory() as db:
            analytics = AnalyticsService(db)
            trending = await analytics.get_trending_games(hours, limit=10)
            
            print("\n📊 TRENDING GAMES:")
            print("=" * 60)
            for i, game in enumerate(trending, 1):
                print(f"{i}. {game['game']} (Articles: {game['article_count']}, Hype: {game['average_hype']:.0f})")
    finally:
        await close_db()


async def cmd_sentiment(hours: int = 24) -> None:
    """Show sentiment distribution."""
    setup_logging()
    await init_db()
    try:
        session_factory = get_session_factory()
        async with session_factory() as db:
            analytics = AnalyticsService(db)
            distribution = await analytics.get_sentiment_distribution(hours)
            
            print("\n💭 SENTIMENT DISTRIBUTION (Last 24h):")
            print("=" * 60)
            for sentiment, count in distribution.items():
                print(f"{sentiment.upper():12} {'█' * (count // 2):50} {count}")
    finally:
        await close_db()


async def cmd_health() -> None:
    """Check system health."""
    setup_logging()
    await init_db()
    try:
        logger.info("Checking system health...")
        
        db_health = await Database.health_check()
        logger.info(f"Database: {'✅ OK' if db_health else '❌ FAILED'}")
        
        settings = get_settings()
        logger.info(f"Environment: {settings.environment}")
        logger.info(f"Debug Mode: {settings.debug}")
        logger.info(f"AI Provider: {settings.ai_provider}")
        
    finally:
        await close_db()


async def main():
    """CLI entry point."""
    if len(sys.argv) < 2:
        print("Usage: python -m app.cli <command> [args]")
        print("\nCommands:")
        print("  scrape              Run one pipeline cycle")
        print("  export [format]     Export articles (json/csv)")
        print("  trending [hours]    Show trending games")
        print("  sentiment [hours]   Show sentiment distribution")
        print("  health              Check system health")
        return

    command = sys.argv[1].lower()
    
    if command == "scrape":
        await cmd_scrape()
    elif command == "export":
        format_type = sys.argv[2] if len(sys.argv) > 2 else "json"
        await cmd_export(format_type)
    elif command == "trending":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        await cmd_trending(hours)
    elif command == "sentiment":
        hours = int(sys.argv[2]) if len(sys.argv) > 2 else 24
        await cmd_sentiment(hours)
    elif command == "health":
        await cmd_health()
    else:
        logger.error(f"Unknown command: {command}")


if __name__ == "__main__":
    asyncio.run(main())
