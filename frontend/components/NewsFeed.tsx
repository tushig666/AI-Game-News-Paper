'use client'

import { useState, useEffect, useRef, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Loader } from 'lucide-react'
import NewsCard from './NewsCard'
import { getNews, NewsItem } from '@/services/api'

interface NewsFeedProps {
  selectedGame: string | null
  isLive: boolean
}

export default function NewsFeed({ selectedGame, isLive }: NewsFeedProps) {
  const [news, setNews] = useState<NewsItem[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)
  const [page, setPage] = useState(1)
  const observerTarget = useRef<HTMLDivElement>(null)

  // Initial load
  useEffect(() => {
    const fetchNews = async () => {
      try {
        setLoading(true)
        setError(null)
        const data = await getNews(1, selectedGame || undefined)
        setNews(data)
        setPage(1)
      } catch (err) {
        setError('Failed to load news. Please try again.')
        console.error(err)
      } finally {
        setLoading(false)
      }
    }

    fetchNews()
  }, [selectedGame])

  // Infinite scroll
  useEffect(() => {
    const observer = new IntersectionObserver(
      async (entries) => {
        if (entries[0].isIntersecting && !loading && isLive) {
          try {
            const nextPage = page + 1
            const data = await getNews(nextPage, selectedGame || undefined)
            setNews((prev) => [...prev, ...data])
            setPage(nextPage)
          } catch (err) {
            console.error('Failed to load more news:', err)
          }
        }
      },
      { threshold: 0.1 }
    )

    if (observerTarget.current) {
      observer.observe(observerTarget.current)
    }

    return () => observer.disconnect()
  }, [page, loading, isLive, selectedGame])

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.6 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="flex items-center gap-2 mb-6">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: 'linear' }}
          className="w-5 h-5 rounded-full border-2 border-neon-cyan border-t-transparent"
        />
        <h2 className="text-xl font-bold neon-text">
          {selectedGame ? selectedGame.toUpperCase() : 'ALL GAMES'} NEWS FEED
        </h2>
        {isLive && (
          <motion.span
            animate={{ opacity: [0.5, 1] }}
            transition={{ duration: 0.5, repeat: Infinity }}
            className="text-xs ml-auto text-neon-green font-bold"
          >
            ● LIVE
          </motion.span>
        )}
      </div>

      {/* Loading state */}
      {loading && news.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-col items-center justify-center py-16 gap-4"
        >
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          >
            <Loader className="w-8 h-8 text-neon-cyan" />
          </motion.div>
          <p className="text-neon-cyan/60">Loading news...</p>
        </motion.div>
      ) : error ? (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-xl p-6 border border-red-400/30 bg-red-400/5"
        >
          <p className="text-red-400">{error}</p>
        </motion.div>
      ) : news.length === 0 ? (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass rounded-xl p-8 text-center"
        >
          <p className="text-neon-cyan/60">No news available at the moment</p>
        </motion.div>
      ) : (
        <>
          {/* News list */}
          <AnimatePresence mode="popLayout">
            {news.map((item, index) => (
              <NewsCard
                key={item.id || `${item.url}-${index}`}
                item={item}
                index={index}
                isLive={isLive}
              />
            ))}
          </AnimatePresence>

          {/* Infinite scroll trigger */}
          <div ref={observerTarget} className="py-8">
            {isLive && (
              <motion.div
                animate={{ opacity: [0.3, 1] }}
                transition={{ duration: 0.5, repeat: Infinity }}
                className="flex items-center justify-center gap-2"
              >
                <div className="w-1.5 h-1.5 rounded-full bg-neon-cyan animate-pulse" />
                <span className="text-sm text-neon-cyan/50">Loading more news...</span>
              </motion.div>
            )}
          </div>
        </>
      )}
    </motion.div>
  )
}
