# 🧠 Game News AI - Premium Frontend

A futuristic, premium gaming news intelligence platform frontend built with Next.js, Tailwind CSS, and Framer Motion.

## 🌟 Features

- **🎯 AI-Powered News Feed**: Real-time gaming news with AI-generated summaries
- **⚡ Live Scraper Status**: Real-time backend scraping statistics and insights
- **🎮 Smart Game Filter**: Filter news by game (Valorant, CS2, Dota 2, LoL, PUBG)
- **🧠 AI Insights Panel**: Trending analysis, sentiment distribution, and hype scores
- **🎨 Futuristic Design**: Glassmorphism, neon colors, cyberpunk aesthetics
- **✨ Smooth Animations**: Framer Motion animations throughout
- **📱 Fully Responsive**: Mobile, tablet, and desktop optimized
- **🚀 Production Ready**: TypeScript, clean architecture, optimized performance

## 🛠️ Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS + Custom CSS
- **Animations**: Framer Motion
- **HTTP Client**: Axios
- **Language**: TypeScript
- **UI Components**: Lucide React Icons

## 📦 Installation

### Prerequisites
- Node.js 18+ (LTS recommended)
- npm or yarn

### Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install

# Copy environment template
cp .env.example .env.local

# (Optional) Edit .env.local to point to your backend
# NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 🚀 Running Locally

```bash
# Development mode
npm run dev
# or
yarn dev

# Open http://localhost:3000 in your browser
```

## 🏗️ Production Build

```bash
# Build for production
npm run build

# Start production server
npm run start

# Output will be optimized and production-ready
```

## 📁 Project Structure

```
frontend/
├── app/
│   ├── layout.tsx          # Root layout with global styles
│   └── page.tsx            # Main dashboard page
│
├── components/
│   ├── Header.tsx          # Navigation header with logo
│   ├── NewsFeed.tsx        # Main news feed with infinite scroll
│   ├── NewsCard.tsx        # Individual news card component
│   ├── ScraperStatus.tsx   # Live scraper status panel
│   ├── GameFilter.tsx      # Game category filter chips
│   └── AIInsights.tsx      # AI insights sidebar
│
├── services/
│   └── api.ts             # API integration layer with mock data fallback
│
├── styles/
│   └── globals.css        # Global styles + Tailwind + custom animations
│
├── utils/                 # Utility functions
├── public/                # Static assets
│
├── package.json           # Dependencies
├── tsconfig.json          # TypeScript config
├── tailwind.config.js     # Tailwind theme
├── next.config.js         # Next.js config
└── postcss.config.js      # PostCSS config
```

## 🎨 Design System

### Color Palette
- **Neon Cyan**: `#00FFFF` - Primary accent
- **Neon Purple**: `#A855F7` - Secondary accent
- **Neon Green**: `#00FF88` - Success/positive
- **Dark BG**: `#0A0E27` - Background
- **Dark Card**: `#1A1F3A` - Card backgrounds

### Components
- **Glass**: Glassmorphism effect with backdrop blur
- **Glow Border**: Gradient neon borders
- **Neon Text**: Gradient text effect
- **Text Glow**: Neon text shadow effect

## 🔄 API Integration

The frontend is designed to work with the backend API at `http://localhost:8000`.

### Required Endpoints

```
GET /api/news?page=1&game=valorant
GET /api/status
GET /api/trending
```

### Mock Data Fallback

If the backend is unavailable, the frontend will automatically serve high-quality mock data, allowing development without a running backend.

## 🎬 Animation Features

- **Page Load**: Cinematic fade-in animations
- **News Cards**: Hover glow and lift effects
- **Staggered Lists**: Smooth sequential animations
- **Background Gradient**: Continuously flowing animated gradients
- **Live Indicators**: Pulsing dot animations
- **Particle Effects**: Floating background particles

## 🔐 Environment Variables

```bash
# .env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📱 Responsive Design

- **Mobile**: Full-screen optimized
- **Tablet**: 2-column layout
- **Desktop**: 4-column grid layout with sidebar

## ⚡ Performance Optimizations

- ✅ Image optimization with Next.js Image
- ✅ Code splitting and lazy loading
- ✅ CSS minification with Tailwind
- ✅ Production build optimization
- ✅ Smooth 60fps animations

## 🎮 Keyboard Shortcuts

- `⌘K` or `Ctrl+K`: Focus search bar

## 📊 Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile browsers: Latest versions

## 🤝 Contributing

1. Create a feature branch
2. Make your changes
3. Test thoroughly
4. Submit a pull request

## 📝 License

MIT - See LICENSE file

## 🙏 Credits

Built with ❤️ for the gaming community

---

**Questions?** Check the [main README](../README.md) for more information.
