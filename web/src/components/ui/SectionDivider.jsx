import { motion } from 'motion/react'

export default function SectionDivider({ title, subtitle }) {
  return (
    <div className="w-full h-full flex flex-col items-center justify-center px-8">
      {/* Accent line */}
      <motion.div
        initial={{ width: 0 }}
        animate={{ width: 80 }}
        transition={{ duration: 0.6, delay: 0.2 }}
        className="h-1 bg-teal-500 rounded-full mb-8"
      />

      <motion.h2
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="font-display text-5xl md:text-6xl font-semibold text-offwhite text-center"
      >
        {title}
      </motion.h2>

      {subtitle && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5, delay: 0.5 }}
          className="mt-4 text-lg text-slate-400 text-center max-w-lg"
        >
          {subtitle}
        </motion.p>
      )}
    </div>
  )
}
