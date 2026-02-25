import { motion } from 'motion/react'

/**
 * Temporary placeholder for slides not yet built.
 * Shows the slide name so navigation can be tested end-to-end.
 */
export default function PlaceholderSlide({ title, slideNumber }) {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center px-8">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.3 }}
        className="text-center"
      >
        <span className="text-navy-800/40 text-sm font-body mb-2 block">
          Slide {slideNumber}
        </span>
        <h2 className="font-body text-4xl font-bold text-navy-800/60">
          {title}
        </h2>
        <div className="mt-4 w-16 h-0.5 bg-white/70 rounded-full mx-auto" />
        <p className="mt-4 text-sm text-navy-800/40">
          Content coming in Phase 5B
        </p>
      </motion.div>
    </div>
  )
}
