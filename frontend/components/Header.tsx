'use client'

import { motion } from 'framer-motion'
import { Zap, Github } from 'lucide-react'
import { useState } from 'react'

interface HeaderProps {
  isLiveMode: boolean
  setIsLiveMode: (value: boolean) => void
}

export default function Header({ isLiveMode, setIsLiveMode }: HeaderProps) {
  const [searchFocus, setSearchFocus] = useState(false)

  return (
    <header className="sticky top-0 z-40 backdrop-blur-2xl bg-dark-bg/50 border-b border-neon-cyan/10">
      <div className="container mx-auto px-4 py-6">
        <div className="flex items-center justify-between">
          {/* Logo and Title */}
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="flex items-center gap-3"
          >
            <div className="relative">
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 4, repeat: Infinity, ease: 'linear' }}
                className="w-8 h-8 rounded-full bg-gradient-to-r from-neon-cyan to-neon-purple shadow-neon-cyan"
              />
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
                className="absolute inset-0 rounded-full border border-neon-cyan shadow-neon-cyan opacity-50"
              />
            </div>
            <div>
              <h1 className="text-2xl font-bold neon-text">GAME NEWS AI</h1>
              <p className="text-xs text-neon-cyan/60">Intelligence Platform</p>
            </div>
          </motion.div>

          {/* Center - Search Bar */}
          <motion.div
            initial={{ opacity: 0, y: -10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="hidden md:block flex-1 max-w-md mx-8"
          >
            <div
              className={`relative transition-all duration-300 ${
                searchFocus ? 'scale-105' : 'scale-100'
              }`}
            >
              <input
                type="text"
                placeholder="Search news... (⌘K)"
                onFocus={() => setSearchFocus(true)}
                onBlur={() => setSearchFocus(false)}
                className="w-full px-4 py-2 rounded-lg bg-dark-card/50 border border-neon-cyan/20 text-white placeholder-neon-cyan/30 focus:outline-none focus:border-neon-cyan/60 focus:shadow-neon-cyan transition-all"
              />
              <span className="absolute right-3 top-2 text-xs text-neon-cyan/40">/</span>
            </div>
          </motion.div>

          {/* Right side controls */}
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="flex items-center gap-4"
          >
            {/* Live Mode Toggle */}
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => setIsLiveMode(!isLiveMode)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg border transition-all duration-300 ${
                isLiveMode
                  ? 'bg-neon-cyan/10 border-neon-cyan/60 text-neon-cyan shadow-neon-cyan'
                  : 'bg-dark-card border-dark-border text-neon-cyan/40'
              }`}
            >
              <motion.div
                animate={{ opacity: isLiveMode ? 1 : 0.5 }}
                transition={{ duration: 0.3 }}
              >
                <Zap size={16} />
              </motion.div>
              <span className="text-sm font-medium">
                {isLiveMode ? 'LIVE' : 'PAUSED'}
              </span>
              {isLiveMode && (
                <motion.div
                  animate={{ opacity: [0.5, 1] }}
                  transition={{ duration: 0.5, repeat: Infinity }}
                  className="w-2 h-2 rounded-full bg-neon-cyan"
                />
              )}
            </motion.button>

            {/* GitHub Link */}
            <motion.a
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.95 }}
              href="https://github.com/tushig666/AI-Game-News-Paper"
              target="_blank"
              rel="noopener noreferrer"
              className="p-2 rounded-lg bg-dark-card hover:bg-dark-card/80 border border-dark-border hover:border-neon-cyan/30 transition-all"
            >
              <Github size={20} className="text-neon-cyan/60 hover:text-neon-cyan" />
            </motion.a>
          </motion.div>
        </div>
      </div>
    </header>
  )
}
