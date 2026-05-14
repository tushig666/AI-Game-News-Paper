'use client'

import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { Brain, TrendingUp, BarChart3 } from 'lucide-react'
import { getTrending } from '@/services/api'

interface Insight {
  title: string
  value: string | number
  trend: 'up' | 'down' | 'stable'
  icon: React.ReactNode
}

export default function AIInsights() {
  const [insights, setInsights] = useState<Insight[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchInsights = async () => {
      try {
        const trendingData = await getTrending()

        const mockInsights: Insight[] = [
          {
            title: 'Trending Right Now',
            value: trendingData.topGame || 'Valorant',
            trend: 'up',
            icon: <TrendingUp size={16} className="text-neon-green" />,
          },
          {
            title: 'Most Mentioned',
            value: `${trendingData.articleCount || 42} articles`,
            trend: 'up',
            icon: <BarChart3 size={16} className="text-neon-purple" />,
          },
          {
            title: 'Sentiment',
            value: trendingData.sentiment || 'Positive',
            trend: trendingData.sentiment === 'Positive' ? 'up' : 'stable',
            icon: <Brain size={16} className="text-neon-cyan" />,
          },
        ]

        setInsights(mockInsights)
      } catch (error) {
        console.error('Failed to fetch insights:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchInsights()
    const interval = setInterval(fetchInsights, 30000)
    return () => clearInterval(interval)
  }, [])

  return (
    <motion.div
      initial={{ opacity: 0, x: 20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.6 }}
      className="space-y-4"
    >
      {/* Header */}
      <div className="glass rounded-xl p-6 border border-neon-purple/20">
        <div className="flex items-center gap-2 mb-4">
          <Brain size={18} className="text-neon-purple" />
          <h2 className="text-lg font-bold text-neon-purple">AI INSIGHTS</h2>
        </div>

        <div className="space-y-3">
          {loading ? (
            <motion.div
              animate={{ opacity: [0.5, 1] }}
              transition={{ duration: 0.5, repeat: Infinity }}
              className="text-sm text-neon-purple/60"
            >
              Analyzing trends...
            </motion.div>
          ) : (
            insights.map((insight, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
                className="p-3 rounded-lg bg-dark-card/50 border border-dark-border hover:border-neon-purple/30 transition-all"
              >
                <div className="flex items-center justify-between mb-1">
                  <span className="text-xs text-neon-purple/60">{insight.title}</span>
                  {insight.icon}
                </div>
                <p className="text-sm font-bold text-white truncate">
                  {insight.value}
                </p>
              </motion.div>
            ))
          )}
        </div>
      </div>

      {/* Sentiment breakdown */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="glass rounded-xl p-6 border border-neon-green/20"
      >
        <h3 className="text-sm font-semibold text-neon-green mb-4">SENTIMENT ANALYSIS</h3>

        <div className="space-y-3">
          {[
            { label: 'Bullish', percentage: 65, color: 'bg-neon-green' },
            { label: 'Neutral', percentage: 25, color: 'bg-neon-cyan' },
            { label: 'Bearish', percentage: 10, color: 'bg-red-400' },
          ].map((item, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: index * 0.05 }}
            >
              <div className="flex justify-between mb-1">
                <span className="text-xs text-neon-green/60">{item.label}</span>
                <span className="text-xs font-mono text-neon-green">
                  {item.percentage}%
                </span>
              </div>
              <div className="h-1.5 bg-dark-border rounded-full overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${item.percentage}%` }}
                  transition={{ duration: 1, delay: index * 0.1 }}
                  className={`h-full ${item.color} rounded-full`}
                />
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* AI Model Info */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="glass rounded-xl p-4 border border-neon-cyan/20 text-center"
      >
        <p className="text-xs text-neon-cyan/60 mb-2">Powered by</p>
        <p className="text-sm font-bold neon-text">Claude 3.5 Sonnet</p>
        <p className="text-xs text-neon-cyan/40 mt-2">Real-time Analysis</p>
      </motion.div>
    </motion.div>
  )
}
