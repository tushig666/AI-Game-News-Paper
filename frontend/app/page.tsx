'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import Header from '@/components/Header'
import NewsFeed from '@/components/NewsFeed'
import ScraperStatus from '@/components/ScraperStatus'
import GameFilter from '@/components/GameFilter'
import AIInsights from '@/components/AIInsights'

export default function Home() {
  const [selectedGame, setSelectedGame] = useState<string | null>(null)
  const [isLiveMode, setIsLiveMode] = useState(true)

  return (
    <div className="min-h-screen w-full">
      {/* Animated background particles */}
      <motion.div
        className="fixed inset-0 -z-10"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 1 }}
      >
        {[...Array(5)].map((_, i) => (
          <motion.div
            key={i}
            className="particle"
            style={{
              width: Math.random() * 300 + 100,
              height: Math.random() * 300 + 100,
              left: `${Math.random() * 100}%`,
              top: `${Math.random() * 100}%`,
            }}
            animate={{
              y: [0, Math.random() * 100 - 50],
              x: [0, Math.random() * 100 - 50],
            }}
            transition={{
              duration: Math.random() * 10 + 15,
              repeat: Infinity,
              repeatType: 'reverse',
            }}
          />
        ))}
      </motion.div>

      {/* Main content */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.8, delay: 0.2 }}
        className="relative"
      >
        <Header isLiveMode={isLiveMode} setIsLiveMode={setIsLiveMode} />

        <main className="container mx-auto px-4 py-8">
          {/* Top section: Status and Controls */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6 mb-8">
            {/* Scraper Status */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.3 }}
              className="lg:col-span-1"
            >
              <ScraperStatus isLive={isLiveMode} />
            </motion.div>

            {/* Game Filter */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: 0.4 }}
              className="lg:col-span-3"
            >
              <GameFilter selectedGame={selectedGame} onSelectGame={setSelectedGame} />
            </motion.div>
          </div>

          {/* Main content: News Feed and AI Insights */}
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
            {/* News Feed */}
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="lg:col-span-3"
            >
              <NewsFeed selectedGame={selectedGame} isLive={isLiveMode} />
            </motion.div>

            {/* AI Insights Sidebar */}
            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6, delay: 0.5 }}
              className="lg:col-span-1"
            >
              <AIInsights />
            </motion.div>
          </div>
        </main>
      </motion.div>
    </div>
  )
}
