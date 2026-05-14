'use client'

import { useEffect, useState } from 'react'
import { motion } from 'framer-motion'
import { Activity, RefreshCw, CheckCircle } from 'lucide-react'
import { getScraperStatus } from '@/services/api'

interface StatusData {
  status: string
  lastUpdated: string
  itemsProcessed: number
  activeScrapers: number
}

interface ScraperStatusProps {
  isLive: boolean
}

export default function ScraperStatus({ isLive }: ScraperStatusProps) {
  const [status, setStatus] = useState<StatusData | null>(null)
  const [loading, setLoading] = useState(true)
  const [timeAgo, setTimeAgo] = useState('just now')

  useEffect(() => {
    const fetchStatus = async () => {
      try {
        const data = await getScraperStatus()
        setStatus(data)
      } catch (error) {
        console.error('Failed to fetch status:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchStatus()
    const interval = setInterval(fetchStatus, 5000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    if (!status) return

    const updateTimeAgo = () => {
      const now = new Date()
      const lastUpdated = new Date(status.lastUpdated)
      const diffSeconds = Math.floor((now.getTime() - lastUpdated.getTime()) / 1000)

      if (diffSeconds < 60) {
        setTimeAgo('just now')
      } else if (diffSeconds < 3600) {
        setTimeAgo(`${Math.floor(diffSeconds / 60)}m ago`)
      } else {
        setTimeAgo(`${Math.floor(diffSeconds / 3600)}h ago`)
      }
    }

    updateTimeAgo()
    const interval = setInterval(updateTimeAgo, 10000)
    return () => clearInterval(interval)
  }, [status])

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="glass rounded-xl p-6 border-l-2 border-l-neon-cyan/50"
    >
      <div className="space-y-4">
        {/* Header */}
        <div className="flex items-center justify-between">
          <motion.div
            animate={{ rotate: isLive ? 360 : 0 }}
            transition={{ duration: 2, repeat: isLive ? Infinity : 0, ease: 'linear' }}
          >
            <Activity
              size={20}
              className={isLive ? 'text-neon-cyan' : 'text-neon-cyan/40'}
            />
          </motion.div>
          <span className="text-xs font-mono text-neon-cyan/60">LIVE_FEED</span>
        </div>

        {/* Status Badge */}
        <div className="flex items-center gap-2">
          <motion.div
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ duration: 0.5, repeat: Infinity }}
            className="w-2 h-2 rounded-full bg-neon-green"
          />
          <span className="text-sm font-medium text-neon-green">
            {isLive ? 'Scraping Active' : 'Paused'}
          </span>
        </div>

        {/* Stats */}
        {status && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="space-y-2 pt-2 border-t border-neon-cyan/10"
          >
            <div className="flex justify-between items-center">
              <span className="text-xs text-neon-cyan/60">Items Processed</span>
              <motion.span
                key={status.itemsProcessed}
                initial={{ scale: 1.2, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                className="text-sm font-mono text-neon-cyan font-bold"
              >
                {status.itemsProcessed}
              </motion.span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-xs text-neon-cyan/60">Active Scrapers</span>
              <span className="text-sm font-mono text-neon-purple">
                {status.activeScrapers}/5
              </span>
            </div>

            <div className="flex justify-between items-center">
              <span className="text-xs text-neon-cyan/60">Last Update</span>
              <span className="text-xs font-mono text-neon-cyan/50">{timeAgo}</span>
            </div>
          </motion.div>
        )}

        {/* Progress bar */}
        <div className="mt-4 space-y-2">
          <div className="h-1 bg-dark-border rounded-full overflow-hidden">
            <motion.div
              animate={{ width: isLive ? '100%' : '30%' }}
              transition={{ duration: 2 }}
              className="h-full bg-gradient-to-r from-neon-cyan to-neon-green"
            />
          </div>
          <p className="text-xs text-neon-cyan/40">
            {isLive ? 'Real-time mode active' : 'Standby mode'}
          </p>
        </div>
      </div>
    </motion.div>
  )
}
