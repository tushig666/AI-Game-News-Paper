'use client'

import { motion } from 'framer-motion'
import { Gamepad2 } from 'lucide-react'

const GAMES = [
  { id: 'valorant', name: 'Valorant', icon: '🎯' },
  { id: 'cs2', name: 'CS2', icon: '🔫' },
  { id: 'dota2', name: 'Dota 2', icon: '⚔️' },
  { id: 'lol', name: 'League of Legends', icon: '👑' },
  { id: 'pubg', name: 'PUBG', icon: '🪂' },
  { id: 'all', name: 'All Games', icon: '🎮' },
]

interface GameFilterProps {
  selectedGame: string | null
  onSelectGame: (game: string | null) => void
}

export default function GameFilter({ selectedGame, onSelectGame }: GameFilterProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.6 }}
      className="glass rounded-xl p-6"
    >
      <div className="flex items-center gap-3 mb-4">
        <Gamepad2 size={18} className="text-neon-purple" />
        <h3 className="text-sm font-semibold text-neon-purple">FILTER BY GAME</h3>
      </div>

      <div className="flex flex-wrap gap-3">
        {GAMES.map((game, index) => {
          const isSelected = selectedGame === game.id || (selectedGame === null && game.id === 'all')

          return (
            <motion.button
              key={game.id}
              initial={{ opacity: 0, scale: 0.8 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.05 }}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={() => onSelectGame(game.id === 'all' ? null : game.id)}
              className={`group relative px-4 py-2 rounded-lg font-medium text-sm transition-all duration-300 ${
                isSelected
                  ? 'bg-gradient-to-r from-neon-cyan/20 to-neon-purple/20 border border-neon-cyan/60 text-neon-cyan shadow-neon-cyan'
                  : 'bg-dark-card/50 border border-dark-border text-neon-cyan/60 hover:border-neon-cyan/40'
              }`}
            >
              <span className="flex items-center gap-2">
                <span>{game.icon}</span>
                {game.name}
              </span>

              {isSelected && (
                <motion.div
                  layoutId="activeGame"
                  className="absolute inset-0 rounded-lg bg-gradient-to-r from-neon-cyan/10 to-neon-purple/10 -z-10"
                  transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                />
              )}
            </motion.button>
          )
        })}
      </div>

      <motion.div
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
        className="mt-4 text-xs text-neon-cyan/40"
      >
        📊 Showing {selectedGame ? `${selectedGame.toUpperCase()} news` : 'all games news'}
      </motion.div>
    </motion.div>
  )
}
