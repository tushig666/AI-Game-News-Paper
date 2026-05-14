"""
Async Processing Pipeline
Orchestrates scraping, analysis, and storage with async task queues.
"""

import asyncio
import logging
from datetime import datetime
from typing import List, Dict
from sqlalchemy.ext.asyncio import AsyncSession

from app.scrapers.base import ArticleData, ScraperPool
from app.scrapers.sites import get_all_scrapers
from app.services.article import (
    ArticleService,
    SummarizationService,
    DuplicateDetectionService,
)
from app.database.connection import get_session_factory

logger = logging.getLogger(__name__)


class ProcessingPipeline:
    """
    Main async pipeline for processing game news articles.
    
    Flow:
    1. Scrape articles from multiple sources
    2. Check for duplicates
    3. Store in database
    4. Summarize with AI
    5. Export results
    """

    def __init__(self, max_concurrent_scrapers: int = 4):
        """Initialize pipeline."""
        self.max_concurrent_scrapers = max_concurrent_scrapers
        self.stats = {
            "scraped": 0,
            "stored": 0,
            "duplicates": 0,
            "summarized": 0,
            "failed": 0,
        }

    async def run(self) -> Dict[str, int]:
        """
        Execute the full processing pipeline.
        
        Returns:
            Statistics dictionary
        """
        logger.info("Starting processing pipeline")
        
        try:
            # Phase 1: Scrape articles
            scraped_articles = await self._scrape_phase()
            self.stats["scraped"] = sum(len(articles) for articles in scraped_articles.values())
            
            # Phase 2: Process and store articles
            stored_count = await self._storage_phase(scraped_articles)
            self.stats["stored"] = stored_count
            
            # Phase 3: Summarize articles
            summarized_count = await self._summarization_phase()
            self.stats["summarized"] = summarized_count
            
            logger.info(f"Pipeline complete: {self.stats}")
            
        except Exception as e:
            logger.error(f"Pipeline error: {str(e)}", exc_info=True)

        return self.stats

    async def _scrape_phase(self) -> Dict[str, List[ArticleData]]:
        """
        Scrape articles from all sources concurrently.
        
        Returns:
            Dictionary mapping source names to article lists
        """
        logger.info("Phase 1: Scraping articles from multiple sources")
        
        scrapers = get_all_scrapers()
        pool = ScraperPool(scrapers, max_concurrent=self.max_concurrent_scrapers)
        
        results = await pool.scrape_all()
        
        for source, articles in results.items():
            logger.info(f"  {source}: {len(articles)} articles")

        return results

    async def _storage_phase(self, scraped_articles: Dict[str, List[ArticleData]]) -> int:
        """
        Store scraped articles in database, checking for duplicates.
        
        Args:
            scraped_articles: Articles from scraping phase
            
        Returns:
            Number of successfully stored articles
        """
        logger.info("Phase 2: Processing and storing articles")
        
        session_factory = get_session_factory()
        stored_count = 0

        async with session_factory() as db:
            article_service = ArticleService(db)
            duplicate_service = DuplicateDetectionService(db)

            for source, articles in scraped_articles.items():
                for article_data in articles:
                    try:
                        # Check if URL already exists
                        if await article_service.article_exists(article_data.url):
                            logger.debug(f"Article already exists: {article_data.url[:50]}")
                            self.stats["duplicates"] += 1
                            continue

                        # Create article
                        article = await article_service.create_article(
                            title=article_data.title,
                            url=article_data.url,
                            body=article_data.body,
                            published_at=article_data.published_at,
                            source_site=source,
                            author=article_data.author,
                            thumbnail_url=article_data.thumbnail_url,
                            tags=article_data.tags,
                            related_games=article_data.category,
                            category=article_data.category,
                            source_id=article_data.source_id,
                        )

                        # Check for duplicates
                        is_duplicate = await duplicate_service.check_duplicate(article)
                        if is_duplicate:
                            self.stats["duplicates"] += 1
                            continue

                        stored_count += 1

                    except Exception as e:
                        logger.error(f"Error storing article from {source}: {str(e)}")
                        self.stats["failed"] += 1

            # Commit all changes
            await db.commit()
            logger.info(f"  Stored {stored_count} articles")

        return stored_count

    async def _summarization_phase(self) -> int:
        """
        Summarize stored articles using AI.
        
        Returns:
            Number of successfully summarized articles
        """
        logger.info("Phase 3: Summarizing articles with AI")
        
        session_factory = get_session_factory()
        summarized_count = 0

        async with session_factory() as db:
            article_service = ArticleService(db)
            summarization_service = SummarizationService(db)

            # Get unprocessed articles
            unprocessed = await article_service.get_unprocessed_articles(limit=50)
            logger.info(f"  Found {len(unprocessed)} unprocessed articles")

            for article in unprocessed:
                try:
                    # Skip very short articles
                    if not article.body or len(article.body.strip()) < 100:
                        await article_service.mark_as_processed(article.id)
                        continue

                    # Summarize with AI
                    summary = await summarization_service.summarize_article(article)
                    
                    if summary:
                        summarized_count += 1

                    await article_service.mark_as_processed(article.id)

                    # Small delay to avoid rate limiting
                    await asyncio.sleep(0.5)

                except Exception as e:
                    logger.error(f"Error summarizing article {article.id}: {str(e)}")
                    self.stats["failed"] += 1

            # Commit all changes
            await db.commit()
            logger.info(f"  Summarized {summarized_count} articles")

        return summarized_count


class PipelineScheduler:
    """
    Scheduler for running the pipeline at regular intervals.
    Manages long-running autonomous agent.
    """

    def __init__(self, interval_minutes: int = 30):
        """
        Initialize scheduler.
        
        Args:
            interval_minutes: Minutes between pipeline runs
        """
        self.interval_minutes = interval_minutes
        self.is_running = False
        self._task: Optional[asyncio.Task] = None

    async def start(self) -> None:
        """Start the scheduler."""
        logger.info(f"Starting pipeline scheduler (interval: {self.interval_minutes} minutes)")
        self.is_running = True
        self._task = asyncio.create_task(self._run_loop())

    async def stop(self) -> None:
        """Stop the scheduler."""
        logger.info("Stopping pipeline scheduler")
        self.is_running = False
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    async def _run_loop(self) -> None:
        """Main scheduler loop."""
        pipeline = ProcessingPipeline()
        
        while self.is_running:
            try:
                await pipeline.run()
                
                # Wait for next interval
                logger.info(f"Waiting {self.interval_minutes} minutes until next run...")
                await asyncio.sleep(self.interval_minutes * 60)

            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Pipeline scheduler error: {str(e)}", exc_info=True)
                # Wait before retrying
                await asyncio.sleep(60)


async def run_pipeline_once() -> Dict[str, int]:
    """Run pipeline once (for manual execution or testing)."""
    pipeline = ProcessingPipeline()
    return await pipeline.run()


async def run_pipeline_daemon(interval_minutes: int = 30) -> None:
    """Run pipeline as daemon with scheduled intervals."""
    scheduler = PipelineScheduler(interval_minutes)
    await scheduler.start()
    
    try:
        # Keep running indefinitely
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        await scheduler.stop()
