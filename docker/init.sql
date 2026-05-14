-- Database initialization script
-- Runs automatically via Docker Compose

-- =====================================================
-- EXTENSIONS
-- =====================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- =====================================================
-- TABLES
-- =====================================================

-- Articles table
CREATE TABLE IF NOT EXISTS articles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title TEXT NOT NULL,
    body TEXT,
    url TEXT UNIQUE,
    author TEXT,
    source TEXT,
    thumbnail TEXT,
    published_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

-- AI summaries table
CREATE TABLE IF NOT EXISTS ai_summaries (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    article_id UUID REFERENCES articles(id) ON DELETE CASCADE,
    summary TEXT,
    bullet_points JSONB,
    sentiment TEXT,
    hype_score INTEGER,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Scraping logs
CREATE TABLE IF NOT EXISTS scraping_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source TEXT,
    status TEXT,
    message TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- INDEXES (SAFE ORDER)
-- =====================================================

CREATE INDEX IF NOT EXISTS idx_articles_title
ON articles(title);

CREATE INDEX IF NOT EXISTS idx_articles_source
ON articles(source);

CREATE INDEX IF NOT EXISTS idx_articles_published_at
ON articles(published_at);

CREATE INDEX IF NOT EXISTS idx_articles_title_trgm
ON articles USING GIN (title gin_trgm_ops);

CREATE INDEX IF NOT EXISTS idx_articles_body_trgm
ON articles USING GIN (body gin_trgm_ops);

-- =====================================================
-- PERMISSIONS
-- =====================================================

GRANT ALL PRIVILEGES ON DATABASE game_news_ai TO "user";
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO "user";
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO "user";