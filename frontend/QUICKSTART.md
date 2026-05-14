# Frontend Quick Start Guide

## 🚀 Get Running in 3 Minutes

### 1. Install Dependencies
```bash
cd frontend
npm install
```

### 2. Set Environment
```bash
cp .env.example .env.local
# Default configuration already points to http://localhost:8000
```

### 3. Start Dev Server
```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

---

## 🌟 What You'll See

### Landing
- Animated logo and header
- Live/Paused mode toggle
- GitHub repository link

### Main Dashboard
**Left Side (75%):**
- Live news feed with infinite scroll
- Real-time AI summaries
- Sentiment indicators (Bullish/Bearish/Neutral/Mixed)
- Hype scores (0-100)
- Source attribution
- Publish timestamps

**Top Controls:**
- Live scraper status panel
- Game category filters (6 chips)
- Real-time statistics

**Right Sidebar (25%):**
- AI Insights panel
- Trending games detection
- Sentiment breakdown chart
- Article count metrics
- Model attribution (Claude 3.5 Sonnet)

---

## 🎨 Visual Features

### Animations
- ✨ Smooth page load fade-in
- 🎯 Hover glow effects on news cards
- 📈 Staggered list animations
- 🌊 Flowing gradient background
- 💫 Floating particles
- ⚡ Pulsing live indicators

### Design
- 🌙 Dark mode only (cyberpunk aesthetic)
- 🔵 Neon cyan primary color
- 💜 Neon purple accents
- 💚 Neon green success state
- ✨ Glassmorphism effect
- 📐 Apple-level spacing and polish

---

## 🔧 Development

### Hot Reload
Changes auto-reload - just save and refresh browser.

### Type Checking
```bash
npm run type-check
```

### Linting
```bash
npm run lint
```

### Production Build
```bash
npm run build
npm run start
```

---

## 📡 API Integration

### Working Without Backend
If your backend isn't running, the frontend automatically serves high-quality mock data:
- Realistic mock news articles
- Authentic scraper statistics
- Trending game data

### Connecting to Backend
Just ensure your backend is running at `http://localhost:8000` and the frontend will connect automatically.

Update `.env.local` if needed:
```
NEXT_PUBLIC_API_URL=http://your-backend:8000
```

---

## 🎮 Feature Breakdown

| Feature | Location | Status |
|---------|----------|--------|
| News Feed | Center panel | ✅ Live |
| Game Filter | Top right | ✅ Live |
| Scraper Status | Top left | ✅ Live |
| AI Insights | Right sidebar | ✅ Live |
| Search Bar | Header | ✅ Live |
| Animations | Everywhere | ✅ Live |
| Responsive Design | All pages | ✅ Live |
| Dark Mode | Entire app | ✅ Live |

---

## 🐛 Troubleshooting

### Port 3000 Already in Use
```bash
npm run dev -- -p 3001
```

### Backend Not Responding
The frontend will show mock data - this is intentional. Backend is optional for development.

### Animations Not Smooth
- Ensure browser hardware acceleration is enabled
- Use Chrome/Edge for best performance
- Check GPU usage in DevTools

### Styles Not Loading
```bash
rm -rf .next
npm run dev
```

---

## 📚 Key Files to Explore

- `app/page.tsx` - Main dashboard layout
- `components/NewsFeed.tsx` - News list with infinite scroll
- `services/api.ts` - Backend integration
- `styles/globals.css` - Global styles and animations
- `tailwind.config.js` - Design system configuration

---

## 💡 Pro Tips

1. **Live Mode**: Toggle with button in header to pause/resume updates
2. **Game Filter**: Click chips to filter by game
3. **Search**: Use ⌘K (Mac) or Ctrl+K (Windows/Linux) to focus search
4. **Infinite Scroll**: News automatically loads as you scroll down
5. **Sentiment Colors**: 
   - 🟢 Bullish (Green)
   - 🔴 Bearish (Red)
   - 🔵 Neutral (Cyan)
   - 🟣 Mixed (Purple)

---

## 🚀 Next Steps

1. Run the frontend (`npm run dev`)
2. Start the backend (see main README)
3. Explore the UI
4. Customize colors in `tailwind.config.js`
5. Add more game categories in `GameFilter.tsx`

**Enjoy your premium gaming news platform!** 🎮✨
