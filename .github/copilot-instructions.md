# AI Game News Intelligence Platform - Development Guide

This project is a **production-grade, enterprise-level autonomous AI system** for game news intelligence.

## Quick Start

### 1. Setup Environment
```bash
cp .env.example .env
# Edit .env with your API keys:
# - ANTHROPIC_API_KEY
# - OPENAI_API_KEY
```

### 2. Start with Docker (Recommended)
```bash
docker-compose up -d
docker-compose logs -f app
```

### 3. Or: Local Development
```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m app.main
```

## Project Structure

```
game-news-ai/
├── app/                           # Main application package
│   ├── __init__.py
│   ├── main.py                   # Application entry point & daemon
│   ├── cli.py                    # CLI tools (scrape, export, trending, health)
│   │
│   ├── config/                   # Configuration
│   │   ├── __init__.py
│   │   └── settings.py          # Pydantic settings, env vars
│   │
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   └── connection.py        # AsyncIO PostgreSQL, session management
│   │
│   ├── models/                   # SQLAlchemy ORM models
│   │   ├── __init__.py
│   │   └── models.py            # Article, Summary, Logs, Trending models
│   │
│   ├── scrapers/                 # Web scraping module
│   │   ├── __init__.py
│   │   ├── base.py              # Abstract scraper base class, RateLimiter
│   │   └── sites.py             # Concrete scrapers (IGN, GameSpot, etc.)
│   │
│   ├── ai/                       # AI service layer
│   │   ├── __init__.py
│   │   └── service.py           # Claude/OpenAI abstraction, factory
│   │
│   ├── services/                 # Business logic services
│   │   ├── __init__.py
│   │   └── article.py           # ArticleService, SummarizationService, Analytics
│   │
│   ├── pipelines/                # Async orchestration
│   │   ├── __init__.py
│   │   └── processing.py        # ProcessingPipeline, PipelineScheduler
│   │
│   ├── exporters/                # Data export services
│   │   ├── __init__.py
│   │   └── service.py           # JSON/CSV export, filtering
│   │
│   ├── utils/                    # Utility modules
│   │   ├── __init__.py
│   │   └── logging_config.py    # Structured logging, ColoredFormatter
│   │
│   └── core/                     # Core utilities
│       └── __init__.py
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures
│   └── test_scrapers.py         # Scraper unit tests
│
├── alembic/                      # Database migrations
│   ├── env.py                   # Migration environment
│   └── versions/                # Migration files
│
├── docker/                       # Docker configuration
│   ├── Dockerfile              # Multi-stage production build
│   └── init.sql                # PostgreSQL initialization
│
├── logs/                         # Application logs (gitignored)
├── exports/                      # Data exports (gitignored)
│
├── .env.example                 # Environment template
├── .gitignore
├── .dockerignore
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── docker-compose.yml           # Full stack (PostgreSQL, Redis, App)
└── README.md                    # Full documentation

```

## Key Features

### 1. **Autonomous Scraping**
- Concurrent multi-site scraping (IGN, GameSpot, PC Gamer, Polygon, Eurogamer)
- Async/await with configurable worker pools
- User-Agent rotation, rate limiting, retry logic
- Duplicate detection by content hash

### 2. **AI Summarization**
- Claude 3.5 Sonnet or GPT-4 Turbo integration
- Sentiment analysis (Bullish/Bearish/Neutral/Mixed)
- Hype scoring (0-100)
- Trending probability calculation
- Token tracking and cost estimation

### 3. **Advanced Architecture**
- Async pipeline: Scrape → Process → Store → Summarize → Export
- SQLAlchemy 2.0 with async/await support
- PostgreSQL with optimized indexes
- Structured logging with rotation
- Configurable via environment variables

### 4. **Enterprise Grade**
- Fully typed Python (PEP 484)
- SOLID principles and Clean Architecture
- Error handling and graceful shutdown
- Health checks and monitoring
- Docker containerization
- Comprehensive documentation

## Common Commands

### Development
```bash
# Run single pipeline cycle
python -m app.cli scrape

# Export results
python -m app.cli export json
python -m app.cli export csv

# View trending games
python -m app.cli trending 24

# View sentiment distribution
python -m app.cli sentiment 24

# Health check
python -m app.cli health

# Run tests
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

### Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down

# Rebuild image
docker-compose build --no-cache
```

## Database

### Connection
- **Local**: `postgresql://user:password@localhost:5432/game_news_ai`
- **Docker**: `postgresql://user:password@postgres:5432/game_news_ai`
- **Async Driver**: `asyncpg`

### Schema
- `articles` - Scraped articles with metadata
- `ai_summaries` - LLM-generated analysis
- `source_sites` - Scraping source configuration
- `scraping_logs` - Activity audit trail
- `trending_scores` - Time-based metrics

## AI Integration

### Claude (Recommended)
- Model: `claude-3-5-sonnet-20241022`
- Cost: $3/1M input, $15/1M output
- Set: `ANTHROPIC_API_KEY`, `AI_PROVIDER=claude`

### OpenAI
- Model: `gpt-4-turbo`
- Cost: $10/1M input, $30/1M output
- Set: `OPENAI_API_KEY`, `AI_PROVIDER=openai`

### Fallback
Automatically falls back if primary provider fails.

## Configuration

Key environment variables:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://...
DATABASE_POOL_SIZE=20

# AI
AI_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-...
AI_TIMEOUT_SECONDS=60

# Scraping
SCRAPER_CONCURRENT_WORKERS=4
SCRAPING_INTERVAL_MINUTES=30

# Environment
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
```

See `.env.example` for all options.

## Performance

- **Scraping**: 50-100 articles/minute (4 workers)
- **AI Summarization**: 10-20 articles/minute
- **Database**: 1000+ writes/minute
- **Memory**: ~200-300MB base

## Code Quality

- Type hints throughout
- PEP 8 compliant
- Docstrings on all modules/classes
- Async/await best practices
- Context managers for resource management

## Extension Points

### Add New Scraper
1. Inherit from `ScraperBase`
2. Implement `async def scrape()`
3. Register in `get_all_scrapers()`

### Add Export Format
1. Implement in `ExportService`
2. Add to export pipeline
3. Update documentation

### Add AI Provider
1. Inherit from `AIServiceBase`
2. Implement `summarize_article()` and `extract_entities()`
3. Register in `AIServiceFactory`

## Deployment

### Docker Compose (Development/Staging)
```bash
docker-compose up -d
```

### Kubernetes (Production)
See README.md for K8s deployment example

### Environment-Specific
- **Development**: 2 workers, DEBUG=True
- **Staging**: 4 workers, DEBUG=False
- **Production**: 8 workers, full monitoring

## Support

- **README.md** - Full documentation
- **Code comments** - Implementation details
- **Type hints** - API contracts
- **Tests** - Usage examples

## Troubleshooting

**API Timeout**: Increase `AI_TIMEOUT_SECONDS`
**Rate Limit**: Reduce `SCRAPER_CONCURRENT_WORKERS`
**Memory**: Check connection pool, reduce batch size
**DB Errors**: Check `DATABASE_URL`, verify PostgreSQL is running

---

For detailed information, see [README.md](README.md)
