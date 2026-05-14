'use client'

import { motion } from 'framer-motion'
import { formatDistanceToNow } from 'date-fns'
import { ExternalLink, Sparkles } from 'lucide-react'
import { NewsItem } from '@/services/api'

interface NewsCardProps {
  item: NewsItem
  index: number
  isLive: boolean
}

const SENTIMENT_COLORS = {
  bullish: 'text-neon-green',
  bearish: 'text-red-400',
  neutral: 'text-neon-cyan',
  mixed: 'text-neon-purple',
}

const GAME_EMOJIS: Record<string, string> = {
  valorant: '🎯',
  cs2: '🔫',
  dota2: '⚔️',
  lol: '👑',
  pubg: '🪂',
}

export default function NewsCard({ item, index, isLive }: NewsCardProps) {
  return (
    <motion.article
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ delay: index * 0.1, duration: 0.5 }}
      whileHover={{ scale: 1.02 }}
      className="glass rounded-xl p-6 border border-neon-cyan/10 hover:border-neon-cyan/40 group cursor-pointer transition-all duration-300 overflow-hidden relative"
    >
      {/* Hover glow effect */}
      <div className="absolute inset-0 bg-gradient-to-r from-neon-cyan/5 to-neon-purple/5 opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

      {/* Live indicator */}
      {isLive && (
        <motion.div
          animate={{ opacity: [0.5, 1] }}
          transition={{ duration: 0.5, repeat: Infinity }}
          className="absolute top-4 right-4 flex items-center gap-1 text-xs text-neon-green"
        >
          <div className="w-1.5 h-1.5 rounded-full bg-neon-green" />
          LIVE
        </motion.div>
      )}

      <div className="relative z-10 space-y-4">
        {/* Header */}
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-lg">
                {GAME_EMOJIS[item.game] || '🎮'}
              </span>
              <span className="text-xs font-mono text-neon-cyan/50 uppercase">
                {item.source}
              </span>
            </div>
            <h3 className="text-lg font-bold leading-tight text-white group-hover:text-neon-cyan transition-colors line-clamp-2">
              {item.title}
            </h3>
          </div>
        </div>

        {/* Summary */}
        <p className="text-sm text-neon-cyan/70 line-clamp-2">
          {item.summary}
        </p>

        {/* Metadata */}
        <div className="flex flex-wrap items-center gap-3 pt-2 border-t border-neon-cyan/10">
          <div className="flex items-center gap-2">
            <span className="text-xs text-neon-cyan/50">
              {formatDistanceToNow(new Date(item.publishedAt), { addSuffix: true })}
            </span>
          </div>

          <div className="flex-1" />

          {/* Sentiment and Hype */}
          <motion.div
            whileHover={{ scale: 1.1 }}
            className="flex items-center gap-2"
          >
            <span className={`text-xs font-mono font-bold ${SENTIMENT_COLORS[item.sentiment as keyof typeof SENTIMENT_COLORS] || 'text-neon-cyan'}`}>
              {item.sentiment?.toUpperCase()}
            </span>
          </motion.div>

          <motion.div
            whileHover={{ scale: 1.1 }}
            className="flex items-center gap-2"
          >
            <Sparkles size={14} className="text-neon-purple" />
            <span className="text-xs font-mono text-neon-purple font-bold">
              {item.hypeScore}/100
            </span>
          </motion.div>
        </div>

        {/* CTA Link */}
        <motion.a
          href={item.url}
          target="_blank"
          rel="noopener noreferrer"
          whileHover={{ x: 5 }}
          className="inline-flex items-center gap-2 text-xs font-semibold text-neon-cyan hover:text-neon-green transition-colors group/link"
        >
          Read Full Article
          <ExternalLink size={14} className="group-hover/link:translate-x-1 transition-transform" />
        </motion.a>
      </div>
    </motion.article>
  )
}
