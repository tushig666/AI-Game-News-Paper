# 🚀 Complete Setup Guide - Game News AI Platform

> Everything you need to run a world-class gaming news intelligence platform locally

---

## 📋 System Requirements

- **Backend**: Python 3.10+
- **Frontend**: Node.js 18+ (LTS)
- **Database**: PostgreSQL 13+ (via Docker)
- **Runtime**: Docker & Docker Compose (optional but recommended)
- **API Keys**: Claude/OpenAI (for AI summarization)

---

## ⚡ Quick Start (5 minutes)

### Option 1: Using Docker Compose (Recommended) 🐳

```bash
# Clone and navigate
git clone https://github.com/tushig666/AI-Game-News-Paper.git
cd AI-Game-News-Paper

# Setup backend
cp .env.example .env
# Edit .env with your API keys:
#   ANTHROPIC_API_KEY=sk-ant-...
#   OPENAI_API_KEY=sk-...

# Start backend services
docker-compose up -d

# Wait ~30 seconds for services to start
sleep 30

# In new terminal: Start frontend
cd frontend
npm install
npm run dev

# Open http://localhost:3000 🎉
```

### Option 2: Local Development (Python + Node)

```bash
# Backend setup
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env with API keys
python -m app.main

# Frontend setup (new terminal)
cd frontend
npm install
npm run dev

# Open http://localhost:3000 🎉
```

---

## 🔧 Detailed Setup

### Backend (Python) ⚙️

#### Step 1: Clone & Navigate
```bash
git clone https://github.com/tushig666/AI-Game-News-Paper.git
cd AI-Game-News-Paper
```

#### Step 2: Virtual Environment
```bash
# macOS/Linux
python3.11 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

#### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

#### Step 4: Database Setup
```bash
# Option A: Using Docker Compose
docker-compose up -d postgres redis

# Option B: Using existing PostgreSQL
# Make sure PostgreSQL is running and accessible
```

#### Step 5: Configure Environment
```bash
cp .env.example .env
```

Edit `.env` with:
```bash
# Database (for Docker)
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/game_news_ai

# AI Services (IMPORTANT)
AI_PROVIDER=claude
ANTHROPIC_API_KEY=sk-ant-your-key-here
OPENAI_API_KEY=sk-your-openai-key-here

# Optional
LOG_LEVEL=INFO
SCRAPER_CONCURRENT_WORKERS=4
```

#### Step 6: Initialize Database
```bash
python -c "
import asyncio
from app.database.connection import Database
asyncio.run(Database.init())
"
```

#### Step 7: Run Backend
```bash
# Development
python -m app.main

# Or with Docker Compose
docker-compose up -d
```

Verify at: http://localhost:8000/health ✅

---

### Frontend (Next.js) 🎨

#### Step 1: Install Node.js
- Download from [nodejs.org](https://nodejs.org) (18+ LTS)
- Verify: `node --version` and `npm --version`

#### Step 2: Navigate to Frontend
```bash
cd frontend
```

#### Step 3: Install Dependencies
```bash
npm install
# or yarn install
```

#### Step 4: Environment Setup
```bash
cp .env.example .env.local
```

Edit `.env.local`:
```bash
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000
```

#### Step 5: Run Development Server
```bash
npm run dev
```

#### Step 6: Open in Browser
```
http://localhost:3000
```

You should see:
- 🧠 AI News Feed
- ⚡ Scraper Status
- 🎮 Game Filters
- 🧠 AI Insights
- ✨ Animations

---

## 📊 Verifying Your Setup

### Backend Health Check ✅
```bash
curl http://localhost:8000/health

# Expected response:
# {"status": "healthy", "timestamp": "..."}
```

### Frontend Response ✅
```bash
curl http://localhost:3000

# Should return HTML with interactive UI
```

### Database Connection ✅
```bash
# If using Docker
docker-compose exec postgres psql -U user -d game_news_ai -c "\dt"

# Should list tables: articles, ai_summaries, source_sites, scraping_logs
```

---

## 🎮 Running Both Together

### Terminal 1: Backend
```bash
# Either Docker
docker-compose up -d

# Or Python
python -m app.main
```

### Terminal 2: Frontend
```bash
cd frontend
npm run dev
```

### Terminal 3: Optional - Monitor Logs
```bash
# Docker logs
docker-compose logs -f app

# Or Python logs
tail -f logs/app.log
```

---

## 🌐 Accessing the Application

| Component | URL | Purpose |
|-----------|-----|---------|
| **Frontend** | http://localhost:3000 | Main UI dashboard |
| **Backend** | http://localhost:8000 | API endpoints |
| **Health** | http://localhost:8000/health | Backend status |
| **Postgres** | localhost:5432 | Database (internal) |
| **Redis** | localhost:6379 | Cache (internal) |

---

## 🔑 API Keys Setup

### Getting Claude API Key
1. Visit [https://console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Create new API key
4. Copy to `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-XXXXXXXXXXXXX
   ```

### Getting OpenAI API Key
1. Visit [https://platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Go to API keys
4. Create new secret key
5. Copy to `.env`:
   ```
   OPENAI_API_KEY=sk-XXXXXXXXXXXXX
   ```

---

## 🐛 Troubleshooting

### Port 3000 Already in Use
```bash
# Frontend on different port
npm run dev -- -p 3001
```

### Port 8000 Already in Use
```bash
# Backend on different port
export PORT=8001
python -m app.main
```

### Backend Won't Connect to Database
```bash
# Check Docker container
docker-compose ps

# Check logs
docker-compose logs postgres

# Restart
docker-compose down -v
docker-compose up -d
```

### Frontend Shows Empty/No News
- ✅ Backend running? Check http://localhost:8000/health
- ✅ API keys configured? Check .env
- ✅ Frontend fallback to mock data if backend unavailable

### Node Modules Issues
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

### Python Dependencies Issues
```bash
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

---

## 📚 Project Structure

```
AI-Game-News-Paper/
│
├── app/                          # Backend Python application
│   ├── main.py                  # Entry point
│   ├── cli.py                   # CLI commands
│   ├── config/                  # Configuration
│   ├── database/                # Database layer
│   ├── models/                  # SQLAlchemy models
│   ├── scrapers/                # Web scrapers
│   ├── ai/                      # AI services
│   ├── services/                # Business logic
│   ├── pipelines/               # Orchestration
│   ├── exporters/               # Export services
│   └── utils/                   # Utilities
│
├── frontend/                     # Next.js Frontend
│   ├── app/                     # Next.js app router
│   ├── components/              # React components
│   ├── services/                # API integration
│   ├── styles/                  # Global styles
│   ├── public/                  # Static assets
│   ├── package.json
│   ├── tsconfig.json
│   ├── tailwind.config.js
│   ├── next.config.js
│   └── README.md
│
├── docker/                       # Docker configs
│   ├── Dockerfile              # Backend image
│   └── init.sql                # Database init
│
├── tests/                        # Test suite
├── alembic/                      # DB migrations
│
├── docker-compose.yml           # Full stack
├── .env.example                 # Env template
├── requirements.txt             # Python deps
├── README.md                    # Main docs
├── README_ja.md                 # Japanese docs
└── SETUP.md                     # This file
```

---

## 🚀 Production Deployment

### Docker Compose to Production
```bash
# Build production images
docker-compose build

# Run with production settings
ENVIRONMENT=production DEBUG=False docker-compose up -d

# Scale backend (if needed)
docker-compose up -d --scale app=3
```

### Kubernetes Deployment
See [README.md](README.md#kubernetes-deployment) for K8s manifests

### Environment Variables for Production
```bash
ENVIRONMENT=production
DEBUG=False
LOG_LEVEL=INFO
DATABASE_POOL_SIZE=50
SCRAPER_CONCURRENT_WORKERS=8
ENABLE_SENTRY=True
SENTRY_DSN=https://...
```

---

## 📖 Additional Resources

| Document | Purpose |
|----------|---------|
| [README.md](README.md) | Project overview & features |
| [README_ja.md](README_ja.md) | Japanese documentation |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System architecture details |
| [frontend/README.md](frontend/README.md) | Frontend documentation |
| [frontend/QUICKSTART.md](frontend/QUICKSTART.md) | Frontend quick start |

---

## ✅ Setup Checklist

- [ ] Clone repository
- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] PostgreSQL 13+ available
- [ ] `.env` configured with API keys
- [ ] Backend running (http://localhost:8000/health)
- [ ] Frontend running (http://localhost:3000)
- [ ] Can see news feed in frontend
- [ ] Game filters working
- [ ] AI insights displayed

---

## 🎉 Success!

If everything is working:
1. ✨ Beautiful cyberpunk UI visible
2. 🔄 Real-time news feed showing
3. 💫 Smooth animations present
4. 📊 Scraper status updating
5. 🎮 Game filters functional
6. 🧠 AI insights panel active

**Congratulations! Your gaming news AI platform is running!** 🚀

---

## 🤝 Support & Contribution

- 📝 Issues: [GitHub Issues](https://github.com/tushig666/AI-Game-News-Paper/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/tushig666/AI-Game-News-Paper/discussions)
- 🔗 Repository: [https://github.com/tushig666/AI-Game-News-Paper](https://github.com/tushig666/AI-Game-News-Paper)

---

**Built with ❤️ by the AI Engineering Team**

Last updated: May 15, 2026
