import { motion } from 'motion/react'

/**
 * Standard slide layout wrapper.
 * Provides consistent padding, max-width, and entrance animation.
 */
export default function SlideLayout({ children, className = '' }) {
  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.3 }}
      className={`w-full h-full flex flex-col justify-center px-8 md:px-16 lg:px-24 py-12 max-w-7xl mx-auto ${className}`}
    >
      {children}
    </motion.div>
  )
}

export function SlideTitle({ children, className = '' }) {
  return (
    <motion.h2
      initial={{ opacity: 0, y: 15 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4, delay: 0.1 }}
      className={`font-body text-3xl md:text-4xl font-bold tracking-tight text-white mb-2 ${className}`}
    >
      {children}
    </motion.h2>
  )
}

export function SlideSubtitle({ children, className = '' }) {
  return (
    <motion.p
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ duration: 0.4, delay: 0.2 }}
      className={`font-body text-base text-slate-400 mb-8 ${className}`}
    >
      {children}
    </motion.p>
  )
}
