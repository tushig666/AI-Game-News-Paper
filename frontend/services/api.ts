import axios from 'axios'

// Types
export interface NewsItem {
  id?: string
  title: string
  url: string
  source: string
  summary: string
  publishedAt: string
  game: string
  sentiment: string
  hypeScore: number
  thumbnailUrl?: string
}

export interface StatusData {
  status: string
  lastUpdated: string
  itemsProcessed: number
  activeScrapers: number
}

export interface TrendingData {
  topGame: string
  articleCount: number
  sentiment: string
}

// Create axios instance
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

// API Service functions
export const getNews = async (
  page: number = 1,
  game?: string
): Promise<NewsItem[]> => {
  try {
    const params = new URLSearchParams()
    params.append('page', page.toString())
    if (game) params.append('game', game)

    const response = await apiClient.get('/api/news', { params })
    
    // Transform and return mock data if API not available
    if (!response.data || response.status === 404) {
      return generateMockNews(page, game)
    }

    return response.data.items || generateMockNews(page, game)
  } catch (error) {
    console.warn('API error, returning mock data:', error)
    return generateMockNews(page, game)
  }
}

export const getScraperStatus = async (): Promise<StatusData> => {
  try {
    const response = await apiClient.get('/api/status')
    
    if (!response.data || response.status === 404) {
      return generateMockStatus()
    }

    return response.data || generateMockStatus()
  } catch (error) {
    console.warn('API error, returning mock status:', error)
    return generateMockStatus()
  }
}

export const getTrending = async (): Promise<TrendingData> => {
  try {
    const response = await apiClient.get('/api/trending')
    
    if (!response.data || response.status === 404) {
      return generateMockTrending()
    }

    return response.data || generateMockTrending()
  } catch (error) {
    console.warn('API error, returning mock trending:', error)
    return generateMockTrending()
  }
}

// Mock data generators
function generateMockNews(page: number, game?: string): NewsItem[] {
  const games = ['valorant', 'cs2', 'dota2', 'lol', 'pubg']
  const sentiments = ['bullish', 'bearish', 'neutral', 'mixed']
  const sources = ['IGN', 'GameSpot', 'PC Gamer', 'Polygon', 'Eurogamer']

  const baseItems = [
    {
      title: 'New Valorant Agent Reveal Sparks Community Debate',
      summary: 'The latest agent announcement has split the community with mixed reactions about balance implications.',
      source: 'IGN',
      game: 'valorant',
    },
    {
      title: 'CS2 Pro Scene Experiences Major Roster Changes',
      summary: 'Top teams shuffle their lineups heading into the next competitive season.',
      source: 'GameSpot',
      game: 'cs2',
    },
    {
      title: 'Dota 2 International Tournament Prize Pool Reaches New Heights',
      summary: 'Crowdfunding mechanism pushes total prize pool beyond previous records.',
      source: 'PC Gamer',
      game: 'dota2',
    },
    {
      title: 'League of Legends Worlds Finals Set New Viewership Record',
      summary: 'Global audience tunes in for the championship match, breaking platform records.',
      source: 'Polygon',
      game: 'lol',
    },
    {
      title: 'PUBG Mobile Announces Massive Map Overhaul',
      summary: 'Complete redesign of classic map brings fresh gameplay opportunities.',
      source: 'Eurogamer',
      game: 'pubg',
    },
  ]

  const items = [...baseItems, ...baseItems].map((item, index) => ({
    id: `news-${page}-${index}`,
    title: item.title,
    url: `https://example.com/news/${index}`,
    source: item.source,
    summary: item.summary,
    publishedAt: new Date(Date.now() - Math.random() * 86400000).toISOString(),
    game: game || item.game,
    sentiment: sentiments[Math.floor(Math.random() * sentiments.length)],
    hypeScore: Math.floor(Math.random() * 100),
    thumbnailUrl: `https://via.placeholder.com/300x200?text=${item.title.substring(0, 20)}`,
  }))

  return items
}

function generateMockStatus(): StatusData {
  return {
    status: 'active',
    lastUpdated: new Date().toISOString(),
    itemsProcessed: Math.floor(Math.random() * 5000) + 1000,
    activeScrapers: Math.floor(Math.random() * 5) + 1,
  }
}

function generateMockTrending(): TrendingData {
  const games = ['Valorant', 'CS2', 'Dota 2', 'League of Legends', 'PUBG']
  return {
    topGame: games[Math.floor(Math.random() * games.length)],
    articleCount: Math.floor(Math.random() * 100) + 20,
    sentiment: ['Positive', 'Neutral', 'Mixed'][Math.floor(Math.random() * 3)],
  }
}

export default apiClient
