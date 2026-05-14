"""
Main Application Entry Point
Async application initialization and startup/shutdown handlers.
"""

import asyncio
import logging
import signal
from contextlib import asynccontextmanager
from typing import Optional

from app.config.settings import get_settings
from app.database.connection import init_db, close_db, Database
from app.utils.logging_config import setup_logging, get_logger
from app.pipelines.processing import PipelineScheduler

logger = get_logger(__name__)


class Application:
    """Main application class."""

    def __init__(self):
        """Initialize application."""
        self.settings = get_settings()
        self.scheduler: Optional[PipelineScheduler] = None
        self._setup()

    def _setup(self) -> None:
        """Setup logging and configuration."""
        setup_logging()
        logger.info(f"Initializing application in {self.settings.environment} mode")
        logger.info(f"Debug mode: {self.settings.debug}")

    async def startup(self) -> None:
        """Application startup sequence."""
        logger.info("=" * 60)
        logger.info("Starting Game News AI Platform")
        logger.info("=" * 60)

        try:
            # Initialize database
            logger.info("Initializing database...")
            await init_db()
            
            # Create tables
            await Database.create_all_tables()
            
            # Health check
            health = await Database.health_check()
            if not health:
                raise RuntimeError("Database health check failed")
            
            logger.info("Database initialized successfully")
            
            # Start pipeline scheduler
            if not self.settings.is_production:
                logger.info("Skipping pipeline scheduler in development mode")
            else:
                logger.info("Starting pipeline scheduler")
                self.scheduler = PipelineScheduler(
                    interval_minutes=self.settings.scraping_interval_minutes
                )
                await self.scheduler.start()

            logger.info("Application startup complete")

        except Exception as e:
            logger.error(f"Startup failed: {str(e)}", exc_info=True)
            raise

    async def shutdown(self) -> None:
        """Application shutdown sequence."""
        logger.info("=" * 60)
        logger.info("Shutting down Game News AI Platform")
        logger.info("=" * 60)

        try:
            # Stop scheduler
            if self.scheduler:
                await self.scheduler.stop()
                logger.info("Pipeline scheduler stopped")

            # Close database
            await close_db()
            logger.info("Database connections closed")

            logger.info("Application shutdown complete")

        except Exception as e:
            logger.error(f"Shutdown error: {str(e)}", exc_info=True)

    @asynccontextmanager
    async def lifespan(self):
        """Async context manager for application lifespan."""
        await self.startup()
        try:
            yield
        finally:
            await self.shutdown()


async def main() -> None:
    """
    Main entry point for the application.
    Runs the pipeline scheduler in daemon mode.
    """
    app = Application()

    # Setup signal handlers for graceful shutdown
    loop = asyncio.get_event_loop()

    def signal_handler(sig):
        logger.info(f"Received signal {sig}, initiating shutdown...")
        asyncio.create_task(app.shutdown())

    for sig in (signal.SIGTERM, signal.SIGINT):
        loop.add_signal_handler(sig, signal_handler, sig)

    async with app.lifespan():
        # Run pipeline scheduler
        from app.pipelines.processing import run_pipeline_daemon
        
        interval = app.settings.scraping_interval_minutes
        logger.info(f"Running pipeline daemon with {interval} minute intervals")
        await run_pipeline_daemon(interval_minutes=interval)


if __name__ == "__main__":
    asyncio.run(main())
